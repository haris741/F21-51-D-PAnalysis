var chart = echarts.init(document.getElementById("main"));
var checkOption1, checkOption2;
checkOption1 = document.getElementById("optionsRadios1");
checkOption2 = document.getElementById("optionsRadios2");
checkOption();
function checkOption() {
  if (checkOption1.checked) {

    var option1=[]
    option1.push(
      {
        name: "Frequency",
        value: 10000,
        textStyle: {
          normal: {
            color: "#4DE600",
          },
        },
      },
      )
    
  } else {
    option1 = [
      {
        name: "Sentimental",
        value: 10000,
        textStyle: {
          normal: {
            color: "#4DE600",
          },
        },
      },
      {
        name: "Deep Learning",
        value: 6181,
        textStyle: {
          normal: {
            color: "#C21A1A",
          },
        },
      },
      {
        name: "Computer Vision",
        value: 4386,
        textStyle: {
          normal: {
            color: "#4DE600",
          },
        },
      },
      {
        name: "Artificial Intelligence",
        value: 4055,
        textStyle: {
          normal: {
            color: "#C21A1A",
          },
        },
      },
      {
        name: "Neural Network",
        value: 3500,
        textStyle: {
          normal: {
            color: "#4DE600",
          },
        },
      },
      {
        name: "Algorithm",
        value: 3333,
        textStyle: {
          normal: {
            color: "#4DE600",
          },
        },
      },
      {
        name: "Model",
        value: 2700,
        textStyle: {
          normal: {
            color: "#C21A1A",
          },
        },
      },
      {
        name: "Supervised",
        value: 2500,
        textStyle: {
          normal: {
            color: "#4DE600",
          },
        },
      },
      {
        name: "Unsupervised",
        value: 2333,
        textStyle: {
          normal: {
            color: "#C21A1A",
          },
        },
      },
      {
        name: "Natural Language Processing",
        value: 1900,
        textStyle: {
          normal: {
            color: "#4DE600",
          },
        },
      },
      {
        name: "Chatbot",
        value: 1800,
        textStyle: {
          normal: {
            color: "#4DE600",
          },
        },
      },
      {
        name: "Virtual Assistant",
        value: 1500,
        textStyle: {
          normal: {
            color: "#C21A1A",
          },
        },
      },
      {
        name: "Speech Recognition",
        value: 1400,
        textStyle: {
          normal: {
            color: "#4DE600",
          },
        },
      },
      {
        name: "Convolutional Neural Network",
        value: 1325,
        textStyle: {
          normal: {
            color: "#4DE600",
          },
        },
      },
      {
        name: "Reinforcement Learning",
        value: 1300,
        textStyle: {
          normal: {
            color: "#C21A1A",
          },
        },
      },
      {
        name: "Training Data",
        value: 1250,
        textStyle: {
          normal: {
            color: "#4DE600",
          },
        },
      },
      {
        name: "Classification",
        value: 1233,
        textStyle: {
          normal: {
            color: "#4DE600",
          },
        },
      },
      {
        name: "Regression",
        value: 1000,
        textStyle: {
          normal: {
            color: "#C21A1A",
          },
        },
      },
      {
        name: "Decision Tree",
        value: 900,
        textStyle: {
          normal: {
            color: "#C21A1A",
          },
        },
      },
      {
        name: "K-Means",
        value: 875,
        textStyle: {
          normal: {
            color: "#4DE600",
          },
        },
      },
      {
        name: "N-Gram Analysis",
        value: 850,
        textStyle: {
          normal: {
            color: "#4DE600",
          },
        },
      },
      {
        name: "Microservices",
        value: 833,
        textStyle: {
          normal: {
            color: "#C21A1A",
          },
        },
      },
      {
        name: "Pattern Recognition",
        value: 790,
        textStyle: {
          normal: {
            color: "#4DE600",
          },
        },
      },
      {
        name: "APIs",
        value: 775,
        textStyle: {
          normal: {
            color: "#4DE600",
          },
        },
      },
      {
        name: "Feature Engineering",
        value: 700,
        textStyle: {
          normal: {
            color: "#C21A1A",
          },
        },
      },
      {
        name: "Random Forest",
        value: 650,
        textStyle: {
          normal: {
            color: "#4DE600",
          },
        },
      },
      {
        name: "Bagging",
        value: 600,
        textStyle: {
          normal: {
            color: "#4DE600",
          },
        },
      },
      {
        name: "Anomaly Detection",
        value: 575,
        textStyle: {
          normal: {
            color: "#4DE600",
          },
        },
      },
      {
        name: "Naive Bayes",
        value: 500,
        textStyle: {
          normal: {
            color: "#4DE600",
          },
        },
      },
      {
        name: "Autoencoder",
        value: 400,
        textStyle: {
          normal: {
            color: "#C21A1A",
          },
        },
      },
      {
        name: "Backpropagation",
        value: 300,
        textStyle: {
          normal: {
            color: "#4DE600",
          },
        },
      },
      {
        name: "TensorFlow",
        value: 290,
        textStyle: {
          normal: {
            color: "#C21A1A",
          },
        },
      },
      {
        name: "word2vec",
        value: 280,
        textStyle: {
          normal: {
            color: "#C21A1A",
          },
        },
      },
      {
        name: "Object Recognition",
        value: 250,
        textStyle: {
          normal: {
            color: "#4DE600",
          },
        },
      },
      {
        name: "Python",
        value: 235,
        textStyle: {
          normal: {
            color: "#4DE600",
          },
        },
      },
      {
        name: "Predictive Analytics",
        value: 225,
        textStyle: {
          normal: {
            color: "#C21A1A",
          },
        },
      },
      {
        name: "Predictive Modeling",
        value: 215,
        textStyle: {
          normal: {
            color: "#4DE600",
          },
        },
      },
      {
        name: "Optical Character Recognition",
        value: 200,
        textStyle: {
          normal: {
            color: "#4DE600",
          },
        },
      },
      {
        name: "Overfitting",
        value: 190,
        textStyle: {
          normal: {
            color: "#C21A1A",
          },
        },
      },
      {
        name: "JavaScript",
        value: 185,
        textStyle: {
          normal: {
            color: "#4DE600",
          },
        },
      },
      {
        name: "Text Analytics",
        value: 180,
        textStyle: {
          normal: {
            color: "#4DE600",
          },
        },
      },
      {
        name: "Cognitive Computing",
        value: 175,
        textStyle: {
          normal: {
            color: "#C21A1A",
          },
        },
      },
      {
        name: "Augmented Intelligence",
        value: 160,
        textStyle: {
          normal: {
            color: "#4DE600",
          },
        },
      },
      {
        name: "Statistical Models",
        value: 155,
        textStyle: {
          normal: {
            color: "#C21A1A",
          },
        },
      },
      {
        name: "Clustering",
        value: 150,
        textStyle: {
          normal: {
            color: "#4DE600",
          },
        },
      },
      {
        name: "Topic Modeling",
        value: 145,
        textStyle: {
          normal: {
            color: "#4DE600",
          },
        },
      },
      {
        name: "Data Mining",
        value: 140,
        textStyle: {
          normal: {
            color: "#4DE600",
          },
        },
      },
      {
        name: "Data Science",
        value: 138,
        textStyle: {
          normal: {
            color: "#C21A1A",
          },
        },
      },
      {
        name: "Artificial Neural Networks",
        value: 125,
        textStyle: {
          normal: {
            color: "#C21A1A",
          },
        },
      },
    ];
  }
  var option = {
    series: [
      {
        type: "wordCloud",
        gridSize: 10,
        maskImage: false,
        sizeRange: [12, 50],
        cursor: "pointer",
        rotationRange: [0, 0],
        shape: "circle",
        width: 800,
        height: 400,
        tooltip: {
          width: 0,
          height: 0,
        },
        drawOutOfBound: false,
        textStyle: {
          normal: {
            color: function () {
              return (
                "rgb(" +
                [
                  Math.round(Math.random() * 160),
                  Math.round(Math.random() * 160),
                  Math.round(Math.random() * 160),
                ].join(",") +
                ")"
              );
            },
          },
        },
        data: option1,
      },
    ],
  };

  chart.setOption(option);

  window.onresize = chart.resize;
}