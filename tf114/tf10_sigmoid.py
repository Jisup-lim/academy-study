import tensorflow as tf
tf.set_random_seed(104)

x_data = [[1,2],[2,3],[3,1],[4,3],[5,3],[6,2]]
y_data = [[0],[0],[0],[1],[1],[1]]

x = tf.compat.v1.placeholder(tf.float32, shape=[None,2])
y = tf.compat.v1.placeholder(tf.float32, shape=[None,1])

w = tf.compat.v1.Variable(tf.random_normal([2,1]), name='weight')
b = tf.compat.v1.Variable(tf.random_normal([1]), name = 'bias')

hypothesis = tf.sigmoid(tf.matmul(x,w) + b)

# cost = tf.reduce_mean(tf.square(hypothesis - y))
cost = -tf.reduce_mean(y*tf.log(hypothesis)+(1-y)*tf.log(1-hypothesis))



train = tf.train.GradientDescentOptimizer(learning_rate=0.01).minimize(cost)
 
predict = tf.cast(hypothesis>0.5,dtype=tf.float32)
accuracy = tf.reduce_mean(tf.cast(tf.equal(predict, y),dtype=tf.float32))

with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())

    for step in range(5001):
        cost_val, _ = sess.run([cost, train], feed_dict = {x:x_data, y:y_data})

        if step % 200 == 0:
            print(step, cost_val) 

    h , c, a = sess.run([hypothesis,predict,accuracy],feed_dict = {x:x_data,y:y_data})
    print("예측값 : \n",h,"\n원래값 : \n", c, "\nacc : ", a)
