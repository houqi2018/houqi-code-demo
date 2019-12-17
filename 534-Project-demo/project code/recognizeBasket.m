function [output_img, g_pi, goal] = recognizeBasket(orig_img,labeled_img, obj_db, threshold)
goal = zeros(2,1);
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
        x1 = mean(c);
        y1 = mean(r);
        x2 = x1 + 100*cos(theta);
        y2 = y1 + 100*sin(theta);
        x3 = x1 - 100*cos(theta);
        y3 = y1 - 100*sin(theta);
        xx = [x1 x2 x3];
        yy = [y1 y2 y3];

        % Plot center and line
        hold on;
        plot(x1, y1, 'r*', 'color', 'blue');
        hold on;
        line(xx, yy, 'color', 'red', 'LineWidth', 1);
        
        
        % Find edge
        tempx = round(x1 -5, 0);
        tempy = round(y1, 0);
        down = tempy;
        up = tempy;
        while labeled_img(down, tempx) ~= 0
           down = down - 1;
           plot(tempx, down, 'r*', 'color', 'green');
        end
        while labeled_img(up,tempx) ~= 0
           up = up + 1;
           plot(tempx, up, 'r*', 'color', 'yellow');
        end
        board_height = up - down;
        ratio_pi_to_m = board_height/1.1;
        g_pi = 9.8 * ratio_pi_to_m;
        goal(1,1) = x1 + 30;
        goal(2,1) = y1 + board_height/4;
        
        % Save image
        set(fh, 'WindowStyle', 'normal');
        img = getimage(fh);
        truesize(fh, [size(img, 1), size(img, 2)]);
        frame = getframe(fh);
        pause(0.5); 
        output_img = frame.cdata;
        break;
        end
    end
    
    % Output original image if there is no match
    if match == 0
        output_img = orig_img;
    end
end
end