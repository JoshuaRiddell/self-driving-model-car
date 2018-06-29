
data = load('ResultsUnityBig.csv');                      % load data
theta = data(:,1);
x = data(:,2);
y = data(:,3);
score = data(:,4);

scatter3(theta, x, y, 100,score,'filled')    % draw the scatter plot

xlabel('Theta')
ylabel('x')
zlabel('y')
cb = colorbar;                                     % create and label the colorbar
cb.Label.String = 'Score';