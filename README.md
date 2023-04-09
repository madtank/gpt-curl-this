# gpt-curl-this

This program let's you say, curl this location, and the results are printed and sent to chatgpt.

## Examples:
curl https://raw.githubusercontent.com/madtank/code/master/jokes/README.md "What type of database is used?"

User: curl https://raw.githubusercontent.com/madtank/code/master/jokes/README.md "What type of database is used?"

Would you like to fetch the content of 'https://raw.githubusercontent.com/madtank/code/master/jokes/README.md'? [y/n]: y

message sent to assistant This is the content you have just fetched using a curl command to 'https://raw.githubusercontent.com/madtank/code/master/jokes/README.md':

<results are printed and sent to gpt>

Assistant: Based on the contents you fetched using the curl command, it seems like you are trying to set up a serverless application using AWS Lambda and DynamoDB which makes use of a random joke API. 

To get started, you will need to follow the steps outlined in the README.md file. You will need to create a S3 bucket and update the configuration file with your bucket name. You will also need to install the AWS SAM CLI if you haven't already. Finally, you can build and deploy your lambda function using SAM CLI.

Once your deployment is successful, you should be able to invoke your lambda function and retrieve random jokes from the API which can be written to the DynamoDB table.

## You can also read local files with file: command.

read a local file and ask about this.

file:text.txt "What is the color of the grass accourding to test.txt file?"

