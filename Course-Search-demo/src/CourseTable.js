import React from 'react';
import './App.css';
import Table from 'react-bootstrap/Table'
import Button from 'react-bootstrap/Button'

class CourseTable extends React.Component {
    renderTableData() {
        let courseName = this.props.courseInfo.number;
        let section = this.props.courseInfo.sections;
        let sectArray = [], item;
        Object.entries(section).forEach(course => {
            // Go to each lecture
            item = {};
            item.courName = courseName;
            item.lec = course[0];
            item.id = course[0];
            item.instructor = course[1].instructor;
            item.location = course[1].location;
            item.time = Object.entries(course[1].time).join();
            item.hasSub = Object.entries(course[1].subsections).length !== 0;
            sectArray.push(item);
            // Go to each subsection
            if (Object.entries(course[1].subsections).length !== 0) {
                let sub = Object.entries(course[1].subsections);
                sub.forEach(subsec => {
                    item = {};
                    item.courName = courseName;
                    item.lec = course[0];
                    item.id = subsec[0];
                    item.instructor = course[1].instructor;
                    item.location = subsec[1].location;
                    item.time = Object.entries(subsec[1].time).join();
                    item.hasSub = true;
                    sectArray.push(item);
                })
            }
        })
        return sectArray.map((rowData, index) => {
           const { courName, lec, id, instructor, location, time, hasSub } = rowData
           return (
              <tr key={ id }>
                 <td><Button variant="secondary"  onClick={() => { 
                    let newCart = this.props.inCart;
                    newCart = newCart.concat([rowData]);
                    this.props.courseTableCallback(newCart);
                    }}>Add</Button>
                 </td>
                 <td >{ id }</td>
                 <td >{ instructor }</td>
                 <td >{ location }</td>
                 <td >{ time }</td>
              </tr>
           )
        })
    }
    render () {
        return (
            <Table style={{marginTop:'5px'}} striped bordered hover size="sm">
                <thead>
                  <tr>
                    <th scope="col"><Button variant="secondary" onClick={() => { 
                        let item = {};
                        item.courName = this.props.courseInfo.number;
                        item.lec = "All";
                        item.id = "All";
                        item.hasSub = Object.entries(this.props.courseInfo.sections).some(cour => { return Object.entries(cour[1].subsections).length !== 0 });
                        let temp = this.props.inCart;
                        temp = temp.concat([item]);
                        this.props.courseTableCallback(temp);
                        }}>Add All</Button></th>
                    <th scope="col">Lecture</th>
                    <th scope="col">Instructor</th>
                    <th scope="col">Location</th>
                    <th scope="col">Time</th>
                  </tr>
                </thead>
                <tbody>
                    {this.renderTableData()}
                </tbody>
            </Table>
      )
   }
}

export default CourseTable;