from fastapi_utils.tasks import repeat_every

# 1 min
@repeat_every(seconds=60 * 1)
async def cron_job():
    print("CronJob....")