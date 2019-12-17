/**
 * @author： Houqi Li, NetID: hli492, StudentID: 9075213778
 *           Mingyi Lu, NetID: mlu69, StudentID: 9075876988
 *           Haozhe Luo, NetID: hluo45, StudentID: 9075267501
 *
 * @section LICENSE
 * Copyright (c) 2012 Database Group, Computer Sciences Department, University of Wisconsin-Madison.
 */

#include <memory>
#include <iostream>
#include "buffer.h"
#include "exceptions/buffer_exceeded_exception.h"
#include "exceptions/page_not_pinned_exception.h"
#include "exceptions/page_pinned_exception.h"
#include "exceptions/bad_buffer_exception.h"
#include "exceptions/hash_not_found_exception.h"

namespace badgerdb { 

BufMgr::BufMgr(std::uint32_t bufs)
	: numBufs(bufs) {
	bufDescTable = new BufDesc[bufs];

  for (FrameId i = 0; i < bufs; i++) 
  {
  	bufDescTable[i].frameNo = i;
  	bufDescTable[i].valid = false;
  }

  bufPool = new Page[bufs];

	int htsize = ((((int) (bufs * 1.2))*2)/2)+1;
  hashTable = new BufHashTbl (htsize);  // allocate the buffer hash table

  clockHand = bufs - 1;
}


// Flushes out all dirty pages 
// and deallocates the buffer pool and the BufDesc table.
BufMgr::~BufMgr() {	
	// flush all valid frames
	for (FrameId i = 0; i < numBufs; i++) {
		if (bufDescTable[i].valid) {
			flushFile(bufDescTable[i].file);
		}
	}
	delete hashTable;
	delete[] bufPool;
	delete[] bufDescTable;
}

// Advance clock to next frame in the buffer pool.
void BufMgr::advanceClock() {
	clockHand = (clockHand + 1) % numBufs;
}

/* Allocates a free frame using the clock algorithm; if necessary, writing 
   a dirty page back to disk. Throws BufferExceededException if all buffer 
   frames are pinned. This private method will get called by the readPage() 
   and allocPage() methods described below. Make sure that if the buffer 
   frame allocated has a valid page in it, you remove the appropriate entry 
   from the hash table.
*/
void BufMgr::allocBuf(FrameId & frame) {
	// track whether alloc successfully
	bool alloc_suc = false;
    unsigned int counter = 0;
	// traverse all frames
    while (counter < numBufs*2 && !alloc_suc) {
		// if the frame is valid
		if (bufDescTable[clockHand].valid) {
			// check pin count, if pin count greater than 0, not ok to allc, 
			// continue
			if (bufDescTable[clockHand].pinCnt > 0) {
                counter++;
                advanceClock();
				continue;
			}
			// check the reference bit, if the refbit is true, set to false 
			// and continue 
            else if (bufDescTable[clockHand].refbit == true) {
				bufDescTable[clockHand].refbit = false;
				counter++;
                advanceClock();
				continue;
            }
			// when pin count is 0 and and refbit is false, replace
			else { 
                // if the frame is dirty, flush it first
				flushFile(bufDescTable[clockHand].file);
				// remove from hash table
				frame = clockHand;
				// set it to successfully allocated
				alloc_suc = true;
			}
		}
		// if the frame is invalid, alloc directly
		else {
			frame = clockHand;
			alloc_suc = true;
		}
	}
	// if after traversing the whole array, still not alloc successfully, 
	// throw exception
	if (!alloc_suc) {
		throw BufferExceededException();
	}
}

/*First check whether the page is already in the buffer pool by invoking the 
  lookup() method, which may throw HashNotFoundException when page is not in 
  the buffer pool, on the hashtable to get a frame number. There are two cases 
  to be handled depending on the outcome of the lookup() call:

• Case 1: Page is not in the buffer pool. Call allocBuf() to allocate a buffer 
  frame and then call the method file->readPage() to read the page from disk 
  into the buffer pool frame. Next, insert the page into the hashtable. 
  Finally, invoke Set() on the frame to set it up properly. Set() will leave 
  the pinCnt for the page set to 1. Return a pointer to the frame containing 
  the page via the page parameter.

• Case 2: Page is in the buffer pool. In this case set the appropriate refbit, 
  increment the pinCnt for the page, and then return a pointer to the frame 
  containing the page via the page parameter.
*/
void BufMgr::readPage(File* file, const PageId pageNo, Page*& page) {
	FrameId frameNo;
	// try looking up the frame in hash table, if success, rad that page
	try {
		hashTable->lookup(file, pageNo, frameNo);
		bufDescTable[frameNo].pinCnt++;
		page = &bufPool[frameNo];
	} catch (HashNotFoundException e) {
		// when the page is not in hash table, alloc one
		allocBuf(frameNo);
        Page tempPage = file->readPage(pageNo);
        bufPool[frameNo] = tempPage;
        // put the page in hash table
		hashTable->insert(file, pageNo, frameNo);
		bufDescTable[frameNo].Set(file, pageNo);
        page = &bufPool[frameNo];
	}
}


/*  Decrements the pinCnt of the frame containing (file, PageNo) and, 
	if dirty == true, sets the dirty bit. Throws PAGENOTPINNED if the 
	pin count is already 0. Does nothing if page is not found in the 
	hash table lookup.
*/
void BufMgr::unPinPage(File* file, const PageId pageNo, const bool dirty) {
	FrameId frameNo;
	hashTable->lookup(file, pageNo, frameNo);
	// Throws exception if pin is already 0
	if (bufDescTable[frameNo].pinCnt <= 0) {
		throw PageNotPinnedException(file->filename(), pageNo, frameNo);
	}
	bufDescTable[frameNo].pinCnt--;
	if (dirty == true) {
		bufDescTable[frameNo].dirty = true;
	} 
}


/*	The first step in this method is to to allocate an empty page 
	in the specified file by invoking the file->allocatePage() method.
	This method will return a newly allocated page. Then allocBuf() 
	is called to obtain a buffer pool frame. Next, an entry is inserted
	into the hash table and Set() is invoked on the frame to set it up
	properly.

	The method returns both the page number of the newly allocated page 
	to the caller via the pageNo parameter and a pointer to the buffer 
	frame allocated for the page via the page parameter.
*/
void BufMgr::allocPage(File* file, PageId &pageNo, Page*& page) {
	Page tempPage;
	// Allocate an empty page first
	tempPage = file->allocatePage();
	FrameId tempFrame;
	allocBuf(tempFrame);
	bufPool[tempFrame] = tempPage;
	// Insert file to hash table
	hashTable->insert(file, tempPage.page_number(), tempFrame);
	bufDescTable[tempFrame].Set(file, tempPage.page_number());
    // Return pageNo and page by reference
	pageNo = tempPage.page_number();
	page = &bufPool[tempFrame];
}


/*  This method deletes a particular page from file. Before deleting
	the page from file, it makes sure that if the page to be deleted
	is allocated a frame in the buffer pool, that frame is freed and
	correspondingly entry from hash table is also removed.
*/
void BufMgr::disposePage(File* file, const PageId PageNo){
    FrameId tempFrame;
    // Find the file in hash table and remoce it
    hashTable->lookup(file, PageNo, tempFrame);
    hashTable->remove(file, PageNo);
    // Also delete the frame from buffer pool and free it
    bufDescTable[tempFrame].Clear();
    file->deletePage(PageNo);
}


/*	Should scan bufTable for pages belonging to the file. For each 
	page encountered it should: (a) if the page is dirty, call 
	file->writePage() to flush the page to disk and then set the 
	dirty bit for the page to false, (b) remove the page from the 
	hashtable (whether the page is clean or dirty) and (c) invoke 
	the Clear() method of BufDesc for the page frame.

	Throws PagePinnedException if some page of the file is pinned.
	Throws BadBufferException if an invalid page belonging to the 
	file is encountered.
*/
void BufMgr::flushFile(const File* file) {
	for (FrameId i = 0; i < numBufs; i++) {
		if (bufDescTable[i].file == file) {
			// Exception if some page of the file is pinned
			if (bufDescTable[i].pinCnt > 0) {
				throw PagePinnedException(file->filename(), 
					bufDescTable[i].pageNo, i);
			}
			// Exception if an invalid page belonging to the 
			if (!bufDescTable[i].valid) {
				throw BadBufferException(i, bufDescTable[i].dirty, 
					bufDescTable[i].valid, bufDescTable[i].refbit);
			}
			// Flush back and remove the file from hashTable if needed
			if (bufDescTable[i].dirty) {
				Page tempPage = bufPool[bufDescTable[i].frameNo];
				bufDescTable[i].file->writePage(tempPage);
				bufDescTable[i].dirty = false;
			}
			// For all files, remove it from hash table and clear frame
			hashTable->remove(file, bufDescTable[i].pageNo);
			bufDescTable[i].Clear();
		}
	}

}

void BufMgr::printSelf(void) 
{
  BufDesc* tmpbuf;
	int validFrames = 0;
  
  for (std::uint32_t i = 0; i < numBufs; i++)
	{
  	tmpbuf = &(bufDescTable[i]);
		std::cout << "FrameNo:" << i << " ";
		tmpbuf->Print();

  	if (tmpbuf->valid == true)
    	validFrames++;
  }

	std::cout << "Total Number of Valid Frames:" << validFrames << "\n";
}

}
