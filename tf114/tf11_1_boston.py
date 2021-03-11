from sklearn.datasets import load_boston
import tensorflow as tf
from sklearn.metrics import r2_score

datasets = load_boston()

x_data = datasets.data
y_data = datasets.target.reshape(-1,1)


print(x_data.shape) # (506, 13)
print(y_data.shape) # (506,)

x = tf.compat.v1.placeholder(tf.float32, shape = [None,13])
y = tf.compat.v1.placeholder(tf.float32, shape = [None,1])

w = tf.compat.v1.Variable(tf.random_normal([13,1]), name = 'weghit')
b = tf.compat.v1.Variable(tf.random_normal([1]),name = 'bias')

# hypothesis = x*w+b
hypothesis = tf.matmul(x, w) + b # matmul = 곱하기

cost = tf.reduce_mean(tf.square(hypothesis - y))
optimizer = tf.train.GradientDescentOptimizer(learning_rate=(0.000001))
train = optimizer.minimize(cost)

sess = tf.compat.v1.Session()
sess.run(tf.compat.v1.global_variables_initializer())

for step in range(2001):
    cost_val, hy_val,_ = sess.run([cost,hypothesis,train], feed_dict={x:x_data,y:y_data})
    if step % 10 == 0:
        print(step, 'cost : ', cost_val,"\n 예측값 : \n", hy_val)
    r2 = r2_score(y_data, hy_val)
    print('R2: ', r2)

sess.close()


# R2:  -2.860261661875775
