clear 
clc
f=fopen('C:\Users\81228\Desktop\资料\人工智能\实验\实验3\iris.data');
Iris=textscan(f,'%f%f%f%f%s','delimiter',',');
fclose(f);
[~,n]=size(Iris);
for i=1:n-1
    data(:,i)=Iris{1,i};
end
[m,n]=size(data);
for i=1:m
    if strcmp(Iris{1,5}{i,1},'Iris-setosa')
        data(i,5:7)=[1 0 0];
    elseif  strcmp(Iris{1,5}{i,1}, 'Iris-versicolor')
        data(i,5:7)=[0 1 0];
    else 
        data(i,5:7)=[0 0 1];
    end
end

%数据归一化处理
x_max=max(data);
x_min=min(data);
data=(data-ones(m,1)*x_min)./(ones(m,1)*(x_max-x_min));

%划分训练样本和测试样本 大约1/2用作训练，1/2用作测试
num=round(m/2/3);
for i=1:3
    temp=data(1+50*(i-1):50*i,:);
    sel=randperm(50,num);
    test(1+num*(i-1):num*i,:)=temp(sel,1:4);
    test_label(1+num*(i-1):num*i,:)=temp(sel,5:7);
    temp(sel,:)=[];
    train(1+(50-num)*(i-1):(50-num)*i,:)=temp(:,1:4);
    train_label(1+(50-num)*(i-1):(50-num)*i,:)=temp(:,5:7);
end

[m,n]=size(train);
alpha=4;%输入神经元数目
beta=10;%隐层神经元数目
lamda=3;%输出神经元数目
rng('shuffle')
W1=rand(alpha,beta);%输入层和隐层之间的权值矩阵
W2=rand(beta,lamda);%隐层和输出层间的权值矩阵
B1=rand(1,beta);%隐层阈值矩阵
B2=rand(1,lamda);%输出层阈值矩阵
B22=B2;
W11=W1;
Eta=1;%学习率
iter_max=10000;%最大迭代次数
iter=1;
%BP神经网络，每次仅针对一个训练样例更新连接权和阈值
while iter<=iter_max
   for i=1:m
    hidden_in=train(i,:)*W1;%隐层输入
    hidden_out=sigmod(hidden_in-B1);%隐层输出
    output_in=hidden_out*W2;%输出层输入
    output_out=sigmod(output_in-B2);%输出层输出
    %计算误差
    E(i)=sum((output_out-train_label(i,:)).^2);%求平方和可用sumsqr函数

    %更新参数,BP神经网络中最核心的部分
   g=output_out.*(1-output_out).*(train_label(i,:)-output_out);%计算输出层神经元的梯度项
   e=hidden_out.*(1-hidden_out).*(g*W2');%计算隐层神经元的梯度项
   Deta_W2=Eta*hidden_out'*g;
   Deta_B2=-Eta*g;
   Deta_W1=Eta*train(i,:)'*e;
   Deta_B1=-Eta*e;
   W1=W1+Deta_W1;
   W2=W2+Deta_W2;
   B1=B1+Deta_B1;
   B2=B2+Deta_B2;
   end
%计算训练集的累积误差
E=mean(E);
if E<1e-4  %目标误差
    iter;
    break
end
if mod(iter,1000)==0
       iter;
end
   iter=iter+1;%更新迭代次数
end

%测试
[result,accuracy]=BP_test(test,test_label,W1,W2,B1,B2);
disp('结果为：')
result'
disp(strcat('准确率为',num2str(accuracy*100),'%'))
function [result,accuracy]=BP_test(test,test_label,W1,W2,B1,B2)
%返回分类的结果
%accuracy准确率
Hidden_in=test*W1;%隐层输入
Hidden_out=sigmod(Hidden_in-B1);%隐层输出
Output_in=Hidden_out*W2;%输入层输入
Output_out=sigmod(Output_in-B2);
[~,result]=max(Output_out,[],2);
[~,index2]=max(test_label,[],2);
right=sum(result==index2);%统计分类正确的个数
total=size(test,1);%总个数
accuracy=right/total;
end
%sigmod函数在matlab里是logsig函数
function [Y]=sigmod(X)
Y=1./(1+exp(-1).^X);
end     
