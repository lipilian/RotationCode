classdef LiuHongAllFunction < handle
    properties
        vSet
        prevFeatures
        prevPoints
        xyzPoints
        xyzPointsDense
        reprojectionErrors
        reprojectionErrorsDense
    end
    
    methods(Static)
        
        function params = calibrateCameraLiuHong(CameraName)
            images = imageSet(fullfile('Calibration', CameraName));
            imageFileNames = images.ImageLocation;
            [imagePoints, boardSize] = detectCheckerboardPoints(imageFileNames);
            squareSizeInMM = 9;
            worldPoints = generateCheckerboardPoints(boardSize,squareSizeInMM);
            I = readimage(images,1); 
            imageSize = [size(I, 1),size(I, 2)];
            params = estimateCameraParameters(imagePoints,worldPoints,'EstimateSkew', true, 'EstimateTangentialDistortion', true ,...
                                                        'ImageSize',imageSize);
            figure;
            showExtrinsics(params);
            save([CameraName, '_parameter'],'params');
        end
        
        function stereoParams = calibrateStereoCameraLiuHong(CameraName1, CameraName2)
            images1 = imageSet(fullfile('Calibration', CameraName1));
            images2 = imageSet(fullfile('Calibration', CameraName2));
            imageFileNames1 = images1.ImageLocation;
            imageFileNames2 = images2.ImageLocation;
            [imagePoints, boardSize, imagesUsed] = detectCheckerboardPoints(imageFileNames1, imageFileNames2);
            squareSize = 10;  % in units of 'millimeters'
            worldPoints = generateCheckerboardPoints(boardSize, squareSize);
            I1 = imread(imageFileNames1{1});
            [mrows, ncols, ~] = size(I1);
            [stereoParams, pairsUsed, estimationErrors] = estimateCameraParameters(imagePoints, worldPoints, ...
                'EstimateSkew', true, 'EstimateTangentialDistortion', true, ...
                'NumRadialDistortionCoefficients', 2, 'WorldUnits', 'millimeters', ...
                'InitialIntrinsicMatrix', [], 'InitialRadialDistortion', [], ...
                'ImageSize', [mrows, ncols]);
            h = figure; showExtrinsics(stereoParams, 'CameraCentric');
        end
                
        function images = readInputImageLiuHong(startIndex, endIndex)
            imageDir = fullfile('Cam_total');
            imds = imageDatastore(imageDir);
            for i = startIndex:1:endIndex
                I = readimage(imds, i);
                images{i - startIndex + 1} = I;
            end
        end
        
        function createFirstViewSetLiuHong(h,image, cameraParams, roi)
            I = undistortImage(image,cameraParams);
            h.prevPoints   = detectSURFFeatures(I);%,'ROI', roi);
            h.prevFeatures = extractFeatures(I, h.prevPoints, 'Upright', true);
            h.vSet = viewSet;
            viewId = 1;
            h.vSet = addView(h.vSet, viewId, 'Points', h.prevPoints, 'Orientation', ...
                eye(3, 'like', h.prevPoints.Location), 'Location', ...
                zeros(1, 3, 'like', h.prevPoints.Location));
        end
        
        function updateVsetLiuHong(h, image, intrinsics, cameraParams1, cameraParams2, roi, index)
            I = undistortImage(image, cameraParams2); %undistort camera image by current cameraParams, which is cameraParams2
            currPoints   = detectSURFFeatures(I); %,'ROI', roi);
            currFeatures = extractFeatures(I, currPoints, 'Upright', true); 
            indexPairs = matchFeatures(h.prevFeatures, currFeatures, ...
                'MaxRatio', .7, 'Unique',  true);
            matchedPoints1 = h.prevPoints(indexPairs(:, 1));
            matchedPoints2 = currPoints(indexPairs(:, 2));
            [relativeOrient, relativeLoc, inlierIdx] = h.helperEstimateRelativePose_TwoViews(...
                matchedPoints1, matchedPoints2, cameraParams1, cameraParams2); %% TODO : rewrite the function
            h.vSet = addView(h.vSet, index, 'Points', currPoints);
            h.vSet = addConnection(h.vSet, index - 1, index, 'Matches', indexPairs(inlierIdx,:));
            prevPose = poses(h.vSet, index-1);
            prevOrientation = prevPose.Orientation{1};
            prevLocation    = prevPose.Location{1};
            orientation = relativeOrient * prevOrientation;
            location    = prevLocation + relativeLoc * prevOrientation;
            h.vSet = updateView(h.vSet, index, 'Orientation', orientation, ...
                'Location', location);
            tracks = findTracks(h.vSet);
            camPoses = poses(h.vSet);
            xyzPoints = triangulateMultiview(tracks, camPoses, intrinsics(1:index));
            [h.xyzPoints, camPoses, h.reprojectionErrors] = bundleAdjustment(xyzPoints, ...
                    tracks, camPoses, intrinsics(1:index), 'FixedViewId', 1, ...
                    'PointsUndistorted', true);
            h.vSet = updateView(h.vSet, camPoses);
            h.prevFeatures = currFeatures;
            h.prevPoints   = currPoints;
        end
        
        function [orientation, location, inlierIdx] = helperEstimateRelativePose_TwoViews...
                (matchedPoints1, matchedPoints2, cameraParams1, cameraParams2)
            if ~isnumeric(matchedPoints1)
                matchedPoints1 = matchedPoints1.Location;
            end

            if ~isnumeric(matchedPoints2)
                matchedPoints2 = matchedPoints2.Location;
            end
            
            for i = 1:100
                [E, inlierIdx] = estimateEssentialMatrix(matchedPoints1, matchedPoints2,...
                    cameraParams1, cameraParams2);
                if sum(inlierIdx) / numel(inlierIdx) < .3
                    continue;
                end
                inlierPoints1 = matchedPoints1(inlierIdx, :);
                inlierPoints2 = matchedPoints2(inlierIdx, :); 
                [orientation, location, validPointFraction] = ...
                    relativeCameraPose(E, cameraParams1, cameraParams2, inlierPoints1(1:2:end, :),...
                    inlierPoints2(1:2:end, :));
                if validPointFraction > .8
                    return;
                end
            end
        end
        
        function displayCameraAndPoints(h)
%             camPoses = poses(h.vSet);
            figure;
%             plotCamera(camPoses, 'Size', 0.2);
%             hold on
            camPoses = poses(h.vSet);
            plotCamera(camPoses, 'Size', 0.2);
            hold on
            goodIdx = (h.reprojectionErrors < 5);
            h.xyzPoints = h.xyzPoints(goodIdx, :);
            pcshow(h.xyzPoints, 'VerticalAxis', 'y', 'VerticalAxisDir', 'down', ...
            'MarkerSize', 45);
            grid on
            hold off
            loc1 = camPoses.Location{1};
            xlim([loc1(1)-1, loc1(1)+1]);
            ylim([loc1(2)-1, loc1(2)+1]);
            zlim([loc1(3)-1, loc1(3)+5]);
            camorbit(0, -30);
        end
        
        function denseReconstruction(h, intrinsics, images, roi, index)
            I = undistortImage(images{1}, intrinsics(1));
            prevPoints = detectMinEigenFeatures(I, 'MinQuality', 0.001);%, 'ROI', roi);
            tracker = vision.PointTracker('MaxBidirectionalError', 1, 'NumPyramidLevels', 6, 'MaxIterations', 30);
            prevPoints = prevPoints.Location;   
            initialize(tracker, prevPoints, I);
            h.vSet = updateConnection(h.vSet, 1, 2, 'Matches', zeros(0, 2));
            h.vSet = updateView(h.vSet, 1, 'Points', prevPoints);
            for i = 2:numel(images)
                I = undistortImage(images{i}, intrinsics(i)); 
                [currPoints, validIdx] = step(tracker, I);
                if i < numel(images)
                    h.vSet = updateConnection(h.vSet, i, i+1, 'Matches', zeros(0, 2));
                end
                h.vSet = updateView(h.vSet, i, 'Points', currPoints);
                matches = repmat((1:size(prevPoints, 1))', [1, 2]);
                matches = matches(validIdx, :);        
                h.vSet = updateConnection(h.vSet, i-1, i, 'Matches', matches);
            end
            tracks = findTracks(h.vSet);
            camPoses = poses(h.vSet);
            h.xyzPointsDense = triangulateMultiview(tracks, camPoses, intrinsics);
            [h.xyzPointsDense, camPoses, h.reprojectionErrorsDense] = bundleAdjustment(...
                h.xyzPointsDense, tracks, camPoses, intrinsics, 'FixedViewId', 1, ...
                'PointsUndistorted', true);
            goodIdx = (h.reprojectionErrorsDense < 5);
            h.xyzPointsDense = h.xyzPointsDense(goodIdx, :);
        end
        
        function displayDenseReconstruction(h)
            figure;
            camPoses = poses(h.vSet);
            plotCamera(camPoses, 'Size', 0.2);
            hold on
            pcshow(h.xyzPointsDense, 'VerticalAxis', 'y', 'VerticalAxisDir', 'down', ...
            'MarkerSize', 45);
            grid on;
            loc1 = camPoses.Location{1};
            xlim([loc1(1)-1, loc1(1)+1]);
            ylim([loc1(2)-1, loc1(2)+1]);
            zlim([loc1(3)-1, loc1(3)+5]);
            camorbit(0, -30);
        end
    end
end
