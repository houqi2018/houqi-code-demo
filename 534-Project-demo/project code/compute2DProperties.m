function db = compute2DProperties(orig_img, labeled_img)
gray_img = im2bw(orig_img, 0.5);
[L,n] = bwlabel(labeled_img);
db = zeros(6,n);

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
end
end