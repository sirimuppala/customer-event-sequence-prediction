Consumer behavior can be represented as sequential data describing the interactions through the time. Examples of these interactions could be the items that the user purchases or views.  Modeling this   customer behavior is essentially modeling the customer journey as series of touchpoints.  Understading the sequence of events that leads to a conversion will add tremendous value to the understanding of conversion funnel, impact of types of touchpoints, and even identify high potential leads for retargeting.

LSTM networks are well researched and understood in the context of solving sequence prediction problems, especially in natural language processing (NLP) and neural machine translation(NMT).  Along similar lines, if a collection of individual sequence of events are organized as a corpus, then an LSTM model can be constructed to predict the target sequence of events (predicted touchpoint sequence that leads to conversion)

In this workshop, we will use LSTM to predict customer’s future events based on the past events customer participated in.  We will use Amazon SageMaker to build, train and deploy the LSTM model.

(Note : Use of LSTM for this use case is based on the session "A novel adoption of LSTM in customer touchpoint prediction" from Strata 2018 conference proceedings. https://conferences.oreilly.com/artificial-intelligence/ai-ca-2018/public/schedule/detail/68831)

Let’s get started. 


### Prerequisites

To run this workshop, you will need 
* An AWS Account 
* IAM user with access to the AWS services : S3, SageMaker, CloudFormation 

### High Level Steps

High level steps to run the workshop :

1. Setup : Execute a cloudformation template that creates a Amazon SageMaker notebook with this git repo downloaded.
2. Build, train and deploy LSTM model : Open the Jupyter notebook created in step 1 and execute notebook cells to examine data, train/deploy the LSTM model and make predictions.

#### Step 1 - Setup

In this step, you will execute a Cloud Formation template to do some initial setup of our environment including creating:

* SageMaker Notebook Instance: This notebook instance will be used as our lab environment after our initial setups required for setting up the workshop.

* SageMaker Notebook lifecycle configuration: Lifecycle configuration created to automatically clone this workshop repository including the notebook instance included for this workshop.

##### Detailed Steps

1.1. Download this git repository by either cloning the repository or downloading the *zip

1.2. Login to the [AWS Console](https://https://console.aws.amazon.com/) and enter your credentials

1.3. Under **Services**, select search for and select [CloudFormation](https://console.aws.amazon.com/cloudformation)

1.4. Click **Create Stack** buttton

   ![CreateStack](images/CreateStack.png)
   
1.5. Under **Select Template**:
    * Click radio button next to 'Upload a template to Amazon S3', then click **Browse**
    * From the local repository cloned to your machine in the detailed step 1, select the file ./prep/Workshop-Prep.yml
    * Click **Open**
    ![CreateStack](images/CreateStack-SpecifyTemplate.png)
    
1.6. Under **Specify Stack Details**, enter: 

   * **Stack Name**: LSTM-WorkshopSetup 

   *  **UniqueID**: Enter *yourinitials* in lower case (Example: jdd)

   ![CreateStack](images/CreateStack-SpecifyStackDetails.png)

1.7. Click **Next**

1.8. Under **Options**, leave all defaults and click '**Next**'

1.9. Under **Review**, scroll to the bottom and check the checkbox acknowledging that CloudFormation might create IAM resources and custom names, then click **Create**

![CreateStack](images/CreateStack-IAMCapabilities.png)

1.10. You will be returned to the CloudFormation console and will see your stack status '**CREATE_IN_PROGRESS**'

![CreateStack](images/CreateStack-CreateInProgress.png)

1.11. After a few minutes, you will see your stack Status change to '**CREATE_COMPLETE**'.  You're encouraged to go explore the resources created as part of this initial setup. 


#### Step 2 - Build, train and deploy LSTM Model
In this step, you will open the SageMaker notebook instance created in Step 1.  
To train, deploy the LSTM model and make predictions execute open the notebook and execute each cell.
  
##### Detailed Steps
 
2.1. Under **Services**, select search for and select [Amazon SageMaker](https://console.aws.amazon.com/sagemaker)
![CreateStack](images/SageMakerDashboard.png) 

2.2. Click "Open Jupyter"

2.3. This shows the contents
![CreateStack](images/JupyterView.png) 

2.4. Click on "customer_event_prediction_lstm.ipynb" to open the notebook.  

2.5. For rest of the workshop, follow instructions in the notebook and execute each cell of the notebook.  
