
class Config:

    #Monitor File path
    MONITERFILE = "monitor.yml"
    
    #DB PSQL
    PS_DATABASE_NAME ="defaultdb"
    PS_USERNAME = "avnadmin"
    PS_PASSWORD ="pwg47mw42l6m1fp5"
    PS_HOST ="pg-task-project-50ec.aivencloud.com"
    PS_PORT= "26508"
    PS_WEBSITE_TABLE_NAME= "websites_status"
    PS_TEST_WEBSITE_TABLE_NAME= "test_websites_status"

    #KAFKA    
    K_HOST = "kafka-website-monitor-project-50ec.aivencloud.com"
    K_PORT = "26510"
    K_SECURITY_PROTOCOL = "SSL"
    K_SSL_CAT_FILE  = "utils/secrets/ca.pem"
    K_SSL_CERT_FILE = "utils/secrets/service.cert"
    K_SSL_KEY_FILE  = "utils/secrets/service.key"
    K_MONITOR_TOPIC = "website-monitor"
    K_REPLICA_FACTOR = 1
    K_NO_PARTITIONS = 1
    

    #REGEX
    URL_REGEX = "(^(http|https)\:\/\/)[a-zA-Z0-9\.\/\?\:@\-_=#]+\.([a-zA-Z]){2,6}([a-zA-Z0-9\.\&\/\?\:@\-_=#])*"

