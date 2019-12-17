%function output_img = recognizeBasket(orig_img, labeled_img, obj_db, threshold)

im1 = im2bw(imread('basket.png'));
im1 = bwmorph(im1, 'dilate', 3);
labeled_img1 = bwlabel(im1);
rgb_img1 = label2rgb(labeled_img1, 'jet', 'k');

im2 = imread('test.png');
im2 = bwmorph(im2, 'dilate', 3);
labeled_img2 = bwlabel(im2);
rgb_img2 = label2rgb(labeled_img2, 'jet', 'k');

orig_img = im2;
labeled_img = labeled_img2;

obj_db = compute2DProperties(im1, labeled_img1);
threshold = [0.85 1.15];
% Calculate corresponding values
gray_img = im2bw(orig_img, 0.5);
[L,n] = bwlabel(labeled_img);
db = zeros(6,n);
fh = figure;
imshow(orig_img);
match = 0;

for i = 1:n
    % Store label
    db(1, i) = i;
    [r, c] = find(L==i);
    rc = [r c];
    
    % Store row and colomn coordinate
    db(2, i) = mean(c);
    db(3, i) = mean(r);
    
    % Calculate a, b, c in formula given in lecture notes
    aa = 0;
    bb = 0;
    cc = 0;
    for ii = 1:size(r)
        aa = aa + (c(ii) - mean(c)).^2;
        bb = bb + (r(ii) - mean(r)) .* (c(ii) - mean(c));
        cc = cc + (r(ii) - mean(r)) .^2;
    end
    bb = 2 .* bb;
    
    % Calculate emin, emax, angle
    emin = 1/2 .* (aa + cc - sqrt(bb.^2 + (aa - cc).^2));
    emax = 1/2 .* (aa + cc + sqrt(bb.^2 + (aa - cc).^2));
    db(4, i) = emin;
    theta = atan(bb ./ (aa - cc)) ./ 2;
    
    % Adjust angle, always keep smaller label
    if ((aa - cc) .* cos(2 .* theta) + bb .* sin(2 .* theta)) < 0
        theta = theta - pi ./ 2;
    end
    
    % Store angle, roundness
    db(5, i) = theta;
    db(6, i) = emin ./ emax;
    
    
    % Check E and Roundness to see if there is a match
    for db_item = 1:size(obj_db, 2)
       
        if (db(4, i) > (obj_db(4, db_item) * threshold(1)))...
            && (db(4, i) < (obj_db(4, db_item) * threshold(2)))...
            && (db(6, i) > (obj_db(6, db_item) * threshold(1)))...
            && (db(6, 1) < (obj_db(6, db_item) * threshold(2)))
        match = 1;
        % Draw line by three points
        x1 = mean(c)
        y1 = mean(r)
        constant = 40;
        x_newcenter = x1 + constant;
        y_newcenter = y1 + constant;
        % (x1,y1) is new center
        x_upperleft = x_newcenter - 40;
        y_upperleft = y_newcenter - 120;
        x_upperright = x_newcenter + 30;
        y_upperright = y_newcenter - 20;
        x_lowerleft = x_newcenter - 40;
        y_lowerleft = y_newcenter + 50;
        x_lowerright = x_newcenter + 30;
        y_lowerright = y_newcenter + 80;
        xx = [x_upperleft x_upperright x_lowerright x_lowerleft x_upperleft]
        yy = [y_upperleft y_upperright y_lowerright y_lowerleft y_upperleft]

        % Plot 4 lines
        hold on;
        plot(x_newcenter, y_newcenter, 'r*', 'color', 'blue');
        hold on;
        line(xx, yy, 'color', 'red', 'LineWidth', 1);

        % Save image
        set(fh, 'WindowStyle', 'normal');
        img = getimage(fh);
        truesize(fh, [size(img, 1), size(img, 2)]);
        frame = getframe(fh);
        pause(0.5); 
        output_img = frame.cdata;
        end
    end
    
    % Output original image if there is no match
    if match == 0
        output_img = orig_img;
    end
end
%end