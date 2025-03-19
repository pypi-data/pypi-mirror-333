# nrequests

nrequests is a simple fork from the main Requests package, with added optional telemetry capabilities.
The main API is identical to the original Requests API.

To disable or define the telemetry collection endpoint you can use the following `requests.conf` file:
```json
{
    "TELEMETRY_ENDPOINT": "http://example.com/endpoint",
    "TELEMETRY_ENABLE": false
}
```

Alternatively you can also set the equivalent environment variables, `TELEMETRY_ENDPOINT` and/or `TELEMETRY_ENABLE`.

Telemetry is enabled by default.

It collects basic OS, Python and system metrics, which can be used for troubleshooting, benchmarking and monitoring.