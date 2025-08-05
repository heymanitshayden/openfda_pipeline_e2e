from datetime import datetime

def transform_record(record):
    def _transform_date(dt):
        try:
            return datetime.strptime(dt, "%Y%m%d").date()
        except Exception as e:
            print(f'Error occurred transforming date {dt}: {e}')
            return None

    adverse_event = {
        "safetyreportid": record.get("safetyreportid", ""),
        "receivedate": _transform_date(record.get("receivedate")),
        "serious": int(record.get("serious", 0)),
        "seriousnessdeath": int(record.get("seriousnessdeath", 0)),
        "seriousnesshospitalization": int(record.get("seriousnesshospitalization", 0))
    }

    drugs = [d.get("medicinalproduct", "") for d in record.get("patient", {}).get("drug", []) if d.get("medicinalproduct")]
    reactions = [r.get("reactionmeddrapt", "") for r in record.get("patient", {}).get("reaction", []) if r.get("reactionmeddrapt")]

    return adverse_event, drugs, reactions