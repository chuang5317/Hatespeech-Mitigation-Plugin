const AWS = require('aws-sdk');
const dynamodb = new AWS.DynamoDB();
const date = new Date();
exports.handler = (event, context, callback) => {
    let body = JSON.parse(event.body);
    dynamodb.putItem({
        TableName: "Hatespeech_incorrect_labels",
        Item: {
            "itemId": {
                "S": context.awsRequestId
            },
            "sentence": { "S": body.sentence},
            "label": { "S": body.label},
            "timestamp": { "S": date.toISOString()}
        }
    }, function(err, data) {
        if (err) {
            console.log(err, err.stack);
            callback(null, {
                statusCode: '500',
                body: err
            });
        } else {
            callback(null, {
                "statusCode": '200',
                "headers": {
                  "Access-Control-Allow-Origin":  "*"
                },
                "body":  JSON.stringify({
            "itemId": context.awsRequestId,
            "sentence": body.sentence,
            "label": body.label,
            "timestamp": date.toISOString()
        })
            });
        }
    })
};
