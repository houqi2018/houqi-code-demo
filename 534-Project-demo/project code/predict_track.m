function [shoot] = predict_track(coordinates, g, goal)
    % Use physics formula to calculate
    time = 0.13;
    dest_y = goal(2,1);
    dest_x = goal(1,1);
    x_velocity = (coordinates(1,1) - coordinates(2,1))/time;
    y_velocity = (coordinates(1,2) - coordinates(2,2) - 0.5 * g * time * time)/time;
    y_dist = dest_y - coordinates(1,2);
    time_need = (-y_velocity + sqrt(y_velocity * y_velocity + 2 * g * y_dist))/g;
    x_arrive = time_need * x_velocity + coordinates(1,1);
    x_diff = abs(x_arrive - dest_x);
    if x_diff <= 30
        shoot = "True";
    else
        shoot = "False";
    end
    t1 = [0:0.13:time_need+0.13];
    t2 = [0:0.13:time_need+0.13];
    x = [coordinates(1,1) + t1 * x_velocity];
    y = [coordinates(1,2) + t2 * y_velocity + 0.5 * g * t2 .* t2];
    
    % Plot a quadratic curve indicating path of the ball
    img = imread('5.png');
    figure; 
    imshow(img);
    hold on, plot(x,y,'-o');
end