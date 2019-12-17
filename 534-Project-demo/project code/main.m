% Clear data and start program
clear all; close all;

%%%%%%%%%%%%%%%%%%%%%%%%%%%%% INPUT DATA %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% User need to specify names of input videos
side_view_video = VideoReader('side view.mp4');
back_view_video = 'back view.MOV';

%%%%%%%%%%%%%%%%%%%%%%%%%%%%% SIDE VIEW %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Extract frames of side view video
numberOfFrames = side_view_video.NumberOfFrames;
outputFolder = sprintf('%s', pwd);
counter = 0;
for frame = 1 : numberOfFrames-1
    if mod(frame, 5) == 0
      this_frame = read(side_view_video, frame);
      tempName = frame/5 -4;
      thisfig = figure();
      thisax = axes('Parent', thisfig);
      image(this_frame, 'Parent', thisax);
      title(thisax, sprintf('Frame #%d', tempName));
      outputBaseFileName = sprintf('%d.png', tempName);
      outputFullFileName = fullfile(outputFolder, outputBaseFileName);
      if counter > 3
        imwrite(this_frame, outputFullFileName, 'png');
      end
      counter = counter + 1;
      if counter == 9
          break;
      end
    end
end

% Empirical thresholds
thres = 60;
erode_thres = 4;
dilute_thres = 2.5;

% Resize the images
i1 = imread('1.png');
i2 = imread('2.png');
i3 = imread('3.png');
i4 = imread('4.png');
i5 = imread('5.png');
imwrite(imresize(i1, 0.5), '1.png');
imwrite(imresize(i2, 0.5), '2.png');
imwrite(imresize(i3, 0.5), '3.png');
imwrite(imresize(i4, 0.5), '4.png');
imwrite(imresize(i5, 0.5), '5.png');
i1 = double(rgb2gray(imread('1.png')));
i2 = double(rgb2gray(imread('2.png')));
i3 = double(rgb2gray(imread('3.png')));
i4 = double(rgb2gray(imread('4.png')));
i5 = double(rgb2gray(imread('5.png')));
img_list = {i1,i2,i3,i4,i5};
result = zeros(size(i1));

% Use Background Split to generate a binary image 
% which tracks movement of the ball
for i=1:size(i1, 1)
    for j=1:size(i1, 2)
        for k = 2:numel(img_list)
            if abs((img_list{k}(i,j)) - (img_list{k-1}(i,j))) > thres
                result(i,j) = 1;
            end
        end
    end
end

% Morph the images, reduce noises
result = bwmorph(result, 'erode', erode_thres);
result = bwmorph(result, 'dilate', dilute_thres);

% Compute the coordinates
[L,n] = bwlabel(result);
rgb_img1 = label2rgb(L, 'jet', 'k');
fh = figure; imshow(result);
coordinates_x = []; coordinates_y = [];
for i = 1:n
    [r, c] = find(L==i);
    rc = [r c];    
    coordinates_x(i) = mean(c);
    coordinates_y(i) = mean(r);

    
% Sort the points, only get top two points
[sortedY, sortIndex] = sort(coordinates_y);
coordinates_y = sortedY; coordinates_x = coordinates_x(sortIndex);
ball_points_array_1 = zeros(2,2);
ball_points_array_1(1,1) = coordinates_x(1);
ball_points_array_1(1,2) = coordinates_y(1);
ball_points_array_1(2,1) = coordinates_x(2);
ball_points_array_1(2,2) = coordinates_y(2);
ball_points_x_coord = [ball_points_array_1(1,1), ball_points_array_1(2,1)]

% Draw the points
hold on;
plot(ball_points_array_1(1,1), ball_points_array_1(1,2), 'r*', 'color', 'green');
plot(ball_points_array_1(2,1), ball_points_array_1(2,2), 'r*', 'color', 'green');
ball_points_array_1

% Compute properties of basket and recognize it
im1 = im2bw(imread('basket.png'));
im1 = bwmorph(im1, 'dilate', 5);
labeled_img1 = bwlabel(im1);
rgb_img1 = label2rgb(labeled_img1, 'jet', 'k');
im2 = imread('1.png');
im2 = rgb2gray(im2);
im2 = edge(im2,'Canny', 0.3);
imshow(im2);
im2 = bwmorph(im2, 'dilate', 1);
labeled_img2 = bwlabel(im2);
obj_db = compute2DProperties(im1, labeled_img1);
threshold = [0.3 1.7];
[output_img, g, goal] = recognizeBasket(im2, labeled_img2, obj_db, threshold);

% Call a method to check if it is a hit
% inside method use physics formula to compute
shoot1 = predict_track(ball_points_array_1, g, goal);

%%%%%%%%%%%%%%%%%%%%%%%%%%%%% BACK VIEW %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Extract frames of back view video
videoObject = VideoReader(back_view_video);
numberOfFrames = videoObject.NumberOfFrames;
figure; [folder, baseFileName, extentions] = fileparts(back_view_video);
outputFolder = sprintf('%s', pwd);
counter = 0;
fontSize=14;
for frame = 1 : numberOfFrames-1
    if mod(frame, 20) == 0
        thisFrame = read(videoObject, frame);
        tempName = frame/20 -2;
        hImage = subplot(1,1,1);
        image(thisFrame);
        caption = sprintf('Frame%4d', tempName);
        title(caption, 'FontSize', fontSize);
        drawnow;
        outputBaseFileName = sprintf('back%d.png', tempName);
        outputFullFileName = fullfile(outputFolder, outputBaseFileName);
        frameWithText = getframe(gca);
        if counter > 1
            imwrite(imrotate(frameWithText.cdata, 270), outputFullFileName, 'png');
        else
            imwrite(imrotate(frameWithText.cdata, 270), 'back0.png', 'png');
        end
        counter = counter + 1;
        if counter == 4
            break;
        end
    end
end

% Empirical thresholds
thres = 60;
erode_thres = 2.5;
dilute_thres = 2.5;
i1 = double(rgb2gray(imread('back1.png')));
i2 = double(rgb2gray(imread('back2.png')));
img_list = {i1,i2};
result = zeros(size(i1));

% Use Background Split to generate a binary image 
% which tracks movement of the ball
for i=1:size(i1, 1)
    for j=1:size(i1, 2)
        for k = 2:numel(img_list)
            if abs((img_list{k}(i,j)) - (img_list{k-1}(i,j))) > thres
                result(i,j) = 1;
            end
        end
    end
end

% Morph the images, reduce noises
result = bwmorph(result, 'erode', erode_thres);
result = bwmorph(result, 'dilate', dilute_thres);
imwrite(result, 'back_result.png');

% Compute the coordinates
result = imread('back_result.png');
[L,n] = bwlabel(result);
fh = figure; imshow(result);
coordinates_x = [];
coordinates_y = [];
for i = 1:n
    [r, c] = find(L==i);
    rc = [r c];    
    coordinates_x(i) = mean(c);
    coordinates_y(i) = mean(r);
    
end
[sortedY, sortIndex] = sort(coordinates_y);
coordinates_y = sortedY;
coordinates_x = coordinates_x(sortIndex);
ball_points_array = zeros(2,2);
ball_points_array(1,1) = coordinates_x(1);
ball_points_array(1,2) = coordinates_y(1);
ball_points_array(2,1) = coordinates_x(2);
ball_points_array(2,2) = coordinates_y(2);
ball_points_x_coord = [ball_points_array(1,1), ball_points_array(2,1)]

% Draw the points
hold on;
plot(ball_points_array(1,1), ball_points_array(1,2), 'r*', 'color', 'green');
plot(ball_points_array(2,1), ball_points_array(2,2), 'r*', 'color', 'green');

% Compute the coordinates
im_back0 = imread('back0.png');
im_back0 = rgb2gray(im_back0);
im_back0 = edge(im_back0,'Canny', 0.47);
im_back0 = bwmorph(im_back0, 'dilate', 3);
[L,n] = bwlabel(im_back0);
fh2 = figure; imshow(im_back0);
coordinates_x = [];
coordinates_y = [];
for i = 1:n
    [r, c] = find(L==i);
    rc = [r c];    
    coordinates_x(i) = mean(c);
    coordinates_y(i) = mean(r);
    
end
[sortedY, sortIndex] = sort(coordinates_y);
coordinates_y = sortedY;
coordinates_x = coordinates_x(sortIndex);
board_center = [round(coordinates_x(1)),round(coordinates_y(1))]

% Plot an area where we think it may be a hit
tempy = round(board_center(1,2), 0);
left = 10;
while im_back0(left, board_center(1,2)) == 0
   left = left + 1;
end
hold on; plot(board_center(1,1), board_center(1,2), 'r*', 'color', 'green');
count = 0;
left = left + abs(board_center(1,1)-left)/2;
left = left + abs(board_center(1,1)-left)/2;
range = [left, left+abs(board_center(1,1)-left)*2]
temp_left = left;
while left < board_center(1,1)
     hold on;
     plot(left, tempy, 'r*', 'color', 'green');
     plot(abs(board_center(1,1)-left) + board_center(1,1), tempy, 'r*', 'color', 'green');
     plot(temp_left, tempy + count, 'r*', 'color', 'green');
     plot(abs(board_center(1,1)-temp_left) + board_center(1,1), tempy + count, 'r*', 'color', 'green');     
     count = count + 1;
     left = left + 1;
end
left = left + abs(board_center(1,1)-left)/2;
for i=1:abs(board_center(1,1)-temp_left)
    plot(left, tempy + count, 'r*', 'color', 'green');
    plot(board_center(1,1)-abs(board_center(1,1)-left) , tempy + count, 'r*', 'color', 'green');
    left = left + 1;
end

% Final check, if both views return hit, then it is a hit, otherwise miss
if ball_points_x_coord(1,1) > range(1,1) && ball_points_x_coord(1,1) < range(1,2) &&...
    ball_points_x_coord(1,2) > range(1,1) && ball_points_x_coord(1,2) < range(1,2) && shoot1 == "True"
    shoot = "True"
else
    shoot = "False"
end

% Clear data and end program
clear all; close all;