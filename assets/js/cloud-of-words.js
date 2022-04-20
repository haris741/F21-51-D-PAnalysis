var chart = echarts.init(document.getElementById('main'));

var option = {
    tooltip: {},
    series: [ {
        type: 'wordCloud',
        gridSize: 2,
        sizeRange: [12, 50],
        rotationRange: [-90, 90],
        shape: 'apple',
        width: 600,
        height: 400,
        drawOutOfBound: true,
        textStyle: {
            normal: {
                color: function () {
                    return 'rgb(' + [
                        Math.round(Math.random() * 160),
                        Math.round(Math.random() * 160),
                        Math.round(Math.random() * 160)
                    ].join(',') + ')';
                }
            },
            emphasis: {
                shadowBlur: 10,
                shadowColor: '#333'
            }
        },
        data: [
            {
                name: 'Machine Learning',
                value: 10000,
                textStyle: {
                    normal: {
                        color: 'black'
                    },
                    emphasis: {
                        color: 'red'
                    }
                }
            },
            {
                name: 'Deep Learning',
                value: 6181
            },
            {
                name: 'Computer Vision',
                value: 4386
            },
            {
                name: 'Artificial Intelligence',
                value: 4055
            },
            {
                name: 'Neural Network',
                value: 3500
            },
            {
                name: 'Algorithm',
                value: 3333
            },
            {
                name: 'Model',
                value: 2700
            },
            {
                name: 'Supervised',
                value: 2500
            },
            {
                name: 'Unsupervised',
                value: 2333
            },
            {
                name: 'Natural Language Processing',
                value: 1900
            },
            {
                name: 'Chatbot',
                value: 1800
            },
            {
                name: 'Virtual Assistant',
                value: 1500
            },
            {
                name: 'Speech Recognition',
                value: 1400
            },
            {
                name: 'Convolutional Neural Network',
                value: 1325
            },
            {
                name: 'Reinforcement Learning',
                value: 1300
            },
            {
                name: 'Training Data',
                value: 1250
            },
            {
                name: 'Classification',
                value: 1233
            },
            {
                name: 'Regression',
                value: 1000
            },
            {
                name: 'Decision Tree',
                value: 900
            },
            {
                name: 'K-Means',
                value: 875
            },
            {
                name: 'N-Gram Analysis',
                value: 850
            },
            {
                name: 'Microservices',
                value: 833
            },
            {
                name: 'Pattern Recognition',
                value: 790
            },
            {
                name: 'APIs',
                value: 775
            },
            {
                name: 'Feature Engineering',
                value: 700
            },
            {
                name: 'Random Forest',
                value: 650
            },
            {
                name: 'Bagging',
                value: 600
            },
            {
                name: 'Anomaly Detection',
                value: 575
            },
            {
                name: 'Naive Bayes',
                value: 500
            },
            {
                name: 'Autoencoder',
                value: 400
            },
            {
                name: 'Backpropagation',
                value: 300
            },
            {
                name: 'TensorFlow',
                value: 290
            },
            {
                name: 'word2vec',
                value: 280
            },
            {
                name: 'Object Recognition',
                value: 250
            },
            {
                name: 'Python',
                value: 235
            },
            {
                name: 'Predictive Analytics',
                value: 225
            },
            {
                name: 'Predictive Modeling',
                value: 215
            },
            {
                name: 'Optical Character Recognition',
                value: 200
            },
            {
                name: 'Overfitting',
                value: 190
            },
            {
                name: 'JavaScript',
                value: 185
            },
            {
                name: 'Text Analytics',
                value: 180
            },
            {
                name: 'Cognitive Computing',
                value: 175
            },
            {
                name: 'Augmented Intelligence',
                value: 160
            },
            {
                name: 'Statistical Models',
                value: 155
            },
            {
                name: 'Clustering',
                value: 150
            },
            {
                name: 'Topic Modeling',
                value: 145
            },
            {
                name: 'Data Mining',
                value: 140
            },
            {
                name: 'Data Science',
                value: 138
            },
            {
                name: 'Semi-Supervised Learning',
                value: 137
            },
            {
                name: 'Artificial Neural Networks',
                value: 125
            }
        ]
    } ]
};

chart.setOption(option);

window.onresize = chart.resize;