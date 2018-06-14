# 前馈神经网络 Feed Forward Neural Network 
训练经常误差采用反向传播算法 （Back Propagation）

    输入层 - 隐藏层 (n) - 输出层
    结点线性变换  output = w*x + b
    结点加激活函数做非线性变换或回归  Sigmoid, tanh, ReLu, Softmax
    
## 误差反向传播算法

通过误差反向传播调整结点的参数w和偏值b

### 代价函数（cost function）
又叫损失函数（lost function），是神经网络优化的目标函数，神经网络训练或者优化的过程就是最小化损失函数的过程（损失函数值小了，对应预测的结果和真实结果的值就越接近

    常用的代价函数： Quadratic Cost 二次代价, Cross-Entropy Cost 交叉熵代价

### 梯度下降 （求输入系数和偏值的下降梯度）
    delta w: -(learning rate * PartialDerivative(w -> Total Error))
    delta b: -(learning rate * PartialDerivative(b -> Total Error))

h为某隐藏结点, 二次代价函数， o为输出结点。

对输出结点求某一连接输入系数和偏值的偏导 

    Total Error = 对所有连接到输出结点的结点，用代价函数计算误差并相加
    对输出结点的某一个连接的输入系数w求偏导：PartialDerivative(w -> Total Error) = PartialDerivative(Outo -> Total Error) * PartialDerivative(Neto -> Outo) * PartialDerivative(w -> Neto) 
    (Outo 是输出结点的输出， Neto是输出结点的净输入，w是该连接的系数)
    PartialDerivative(Outo -> Total Error): 是代价函数的导数
    PartialDerivative(Neto -> Outo): 是激活函数的导数
    PartialDerivative(w -> Neto):  Neto = w * Outh + b，所以对w求的偏导数是 Outh
    (Outh是该连接对应隐藏结点的输出， b为该连接的偏置)
    该隐藏结点的 node delta = PartialDerivative(Neto -> Total Error) = PartialDerivative(Outo -> Total Error) * PartialDerivative(Neto -> Outo)
    所以Total Error对w的偏导 = node delta * Outh

    对该连接的b求偏导：PartialDerivative(b -> Total Error) = PartialDerivative(Outo -> Total Error) * PartialDerivative(Neto -> Outo) * PartialDerivative(b -> Neto)
    PartialDerivative(b -> Neto)： Neto = w * Outh + b，所以对b求的偏导数是 1
    所以Total Error对b的偏导 = node delta * 1 = node delta  

对隐藏结点求输入系数和偏值的偏导 

    Error(i)是该隐藏结点连接到某个输出结点的误差
    
    对隐藏结点的某一个连接的输入系数wh求偏导：PartialDerivative(wh -> Total Error) = PartialDerivative(Outh -> Total Error) * PartialDerivative(Neth -> Outh) * PartialDerivative(wh -> Neth)
    (Outh 是为该隐藏结点的输出， Neth是该隐藏结点的净输入，wh是与某前结点连接的输入系数)
    PartialDerivative(Outh -> Total Error)： 等于当前连接的前面的结点输出对各个输出结点误差求偏导，再相加。 即n个PartialDerivative(Outh -> Error(i))相加 (i取值1到n)
        PartialDerivative(Outh -> Error(i)) = PartialDerivative(Neto -> Error(i)) * PartialDerivative(Outh -> Neto) = 该隐藏节点的node delta * w
            PartialDerivative(Neto -> Error(i): 即该隐藏结点的node delta
            PartialDerivative(Outh -> Neto)：Neto = w * Outh + b，所以对Outh求的偏导数是 w (Error(i)对应的连接的输出节点的输入参数)
    所以  PartialDerivative(Outh -> Total Error) = 所有隐藏结点的(node delta * w)后再相加    
    PartialDerivative(Neth -> Outh)：是激活函数的导数
    PartialDerivative(w -> Neth):  Neth = w * PreNodeOut + b，所以对w求的偏导数是 PreNodeOut
    (PreOut是该链接对应的前面结点的输出)
    对应连接到该隐藏结点的某个结点的node delta = (所有隐藏结点的(node delta * w)后再相加) * 激活函数的导数
    所以Total Error对wh的偏导 = (连接到该隐藏结点的某个结点的node delta) * PreNodeOut
    
    对隐藏结点的该连接的输入偏置bh求偏导：PartialDerivative(bh -> Total Error) = PartialDerivative(Outh -> Total Error) * PartialDerivative(Neth -> Outh) * PartialDerivative(bh -> Neth)
    同理Total Error对bh的偏导 = (连接到该隐藏结点的某个结点的node delta) * 1 = 连接到该隐藏结点的某个结点的node delta

## 参考
https://blog.csdn.net/zchang81/article/details/78119583

https://mattmazur.com/2015/03/17/a-step-by-step-backpropagation-example/
 



