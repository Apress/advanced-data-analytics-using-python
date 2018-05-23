from numpy import loadtxt, where, zeros, e, array, log, ones, mean, where
from pylab import scatter, show, legend, xlabel, ylabel, plot
from scipy.optimize import fmin_bfgs


def sigmoid(X):
    '''Compute the sigmoid function '''
    #d = zeros(shape=(X.shape))

    den = 1.0 + e ** (-1.0 * X)

    d = 1.0 / den

    return d


def compute_cost(theta, X, y):
    '''
    Comput cost for logistic regression
    '''
    #Number of training samples

    theta.shape = (1, 3)

    m = y.size

    h = sigmoid(X.dot(theta.T))

    J = (1.0 / m) * ((-y.T.dot(log(h))) - ((1.0 - y.T).dot(log(1.0 - h))))

    return - 1 * J.sum()


def compute_grad(theta, X, y):

    #print theta.shape

    theta.shape = (1, 3)

    grad = zeros(3)

    h = sigmoid(X.dot(theta.T))

    delta = h - y

    l = grad.size

    for i in range(l):
        sumdelta = delta.T.dot(X[:, i])
        grad[i] = (1.0 / m) * sumdelta * - 1

    theta.shape = (3,)

    return  grad


#load the dataset
data = loadtxt('ex2data1.txt', delimiter=',')

X = data[:, 0:2]
y = data[:, 2]

pos = where(y == 1)
neg = where(y == 0)
scatter(X[pos, 0], X[pos, 1], marker='o', c='b')
scatter(X[neg, 0], X[neg, 1], marker='x', c='r')
xlabel('Exam 1 score')
ylabel('Exam 2 score')
legend(['Not Admitted', 'Admitted'])
#show()

m, n = X.shape

y.shape = (m, 1)

#Add intercept term to x and X_test
it = ones(shape=(m, 3))
it[:, 1:3] = X


def decorated_cost(it, y):
    def f(theta):
        return compute_cost(theta, it, y)

    def fprime(theta):
        return compute_grad(theta, it, y)

    #Initialize theta parameters
    theta = zeros(3)

    return fmin_bfgs(f, theta, fprime, disp=True, maxiter=400)

decorated_cost(it, y)
theta = [-25.161272, 0.206233, 0.201470]


#Plotting the decision boundary
plot_x = array([min(it[:, 1]) - 2, max(it[:, 2]) + 2])
plot_y = (- 1.0 / theta[2]) * (theta[1] * plot_x + theta[0])
plot(plot_x, plot_y)
legend(['Decision Boundary', 'Not admitted', 'Admitted'])
#show()

prob = sigmoid(array([1.0, 45.0, 85.0]).dot(array(theta).T))
print 'For a student with scores 45 and 85, we predict and admission ' + \
    'probability of %f' % prob


def predict(theta, X):
    '''Predict whether the label
    is 0 or 1 using learned logistic
    regression parameters '''
    m, n = X.shape
    p = zeros(shape=(m, 1))

    h = sigmoid(X.dot(theta.T))

    for it in range(0, h.shape[0]):
        if h[it] > 0.5:
            p[it, 0] = 1
        else:
            p[it, 0] = 0

    return p

#Compute accuracy on our training set
p = predict(array(theta), it)
print 'Train Accuracy: %f' % ((y[where(p == y)].size / float(y.size)) * 100.0)
