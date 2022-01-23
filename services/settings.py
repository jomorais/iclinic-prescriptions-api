dependent_services_settings = {
    "clinics-service": {
        "host": "https://mock-api-challenge.dev.iclinic.com.br",
        "auth_token": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyLCJzZXJ2aWNlIjoiY2xpbmljcyJ9.r3w8KS4LfkKqZhOUK8YnIdLhVGJEqnReSClLCMBIJRQ",
        "path": "/clinics/",
        "retries": 3,
        "timeout": 5,
        "cache_ttl": 259200
    },
    "patients-service": {
        "host": "https://mock-api-challenge.dev.iclinic.com.br",
        "auth_token": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyLCJzZXJ2aWNlIjoicGF0aWVudHMifQ.Pr6Z58GzNRtjX8Y09hEBzl7dluxsGiaxGlfzdaphzVU",
        "path": "/patients/",
        "retries": 2,
        "timeout": 3,
        "cache_ttl": 43200
    },
    "physicians-service": {
        "host": "https://mock-api-challenge.dev.iclinic.com.br",
        "auth_token": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyLCJzZXJ2aWNlIjoicGh5c2ljaWFucyJ9.Ei58MtFFGBK4uzpxwnzLxG0Ljdd-NQKVcOXIS4UYJtA",
        "path": "/physicians/",
        "retries": 2,
        "timeout": 4,
        "cache_ttl": 172800
    },
    "metrics-service": {
        "host": "https://mock-api-challenge.dev.iclinic.com.br",
        "auth_token": "Bearer SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c",
        "path": "/metrics/",
        "retries": 5,
        "timeout": 6,
        "cache_ttl": 0
    }
}