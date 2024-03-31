from fastapi import FastAPI, Request, Query, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from sqlmodel import SQLModel, Field, create_engine, Session
from datetime import datetime
from datetime import timedelta
from typing import List
import json

app = FastAPI()

# 添加 CORS 中间件，只允许特定的来源
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源
    # allow_origins=["https://cloud.io.net"],  # 只允许来自 cloud.io.net 的请求，你还得加个你自己的域名
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有 HTTP 方法
    allow_headers=["*"],  # 允许所有头部
)


# 定义数据模型
class Data(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    user_id: str
    timestamp: str
    device_data: str


# 创建数据库引擎
DATABASE_URL = "sqlite:///./dage.db"  # 修改为新的数据库 URL
engine = create_engine(DATABASE_URL)

# 创建数据库表（如果不存在）
SQLModel.metadata.create_all(engine)
templates = Jinja2Templates(directory="templates")


def format_timestamp(value):
    timestamp = int(value) / 1000  # 将毫秒转换为秒
    # 加上 8 小时的时区偏移量
    adjusted_time = datetime.fromtimestamp(timestamp) + timedelta(hours=8)
    return adjusted_time.strftime("%Y-%m-%d %H:%M:%S")

templates.env.filters["format_timestamp"] = format_timestamp


def parse_device_data(value):
    print(value)
    return value


templates.env.filters["parse_device_data"] = parse_device_data


@app.post("/ionet")
async def post_data(request: Request, user_id: str = Header(None), timestamp: str = Header(None)):
    data = await request.json()
    # 检查数据库中是否已存在相同的 user_id 和 timestamp 的记录
    with Session(engine) as session:
        existing_data = session.query(Data).filter(Data.user_id == user_id, Data.timestamp == timestamp).first()
        if existing_data is None:
            # 如果不存在，则插入新数据
            db_data = Data(user_id=user_id, timestamp=timestamp, device_data=json.dumps(data))
            session.add(db_data)
            session.commit()
            return {"message": "数据已接收并存储", "data": data}
        else:
            # 如果已存在，不进行插入操作
            return {"message": "有相同用户ID和时间戳的数据已存在", "data": data}

@app.get("/", response_model=List[Data])
async def root(request: Request, user_id: str = Query(None)):
    with Session(engine) as session:
        if user_id:
            data = session.query(Data).filter(Data.user_id == user_id).first()
        else:
            data = None

    if data:
        data.device_data = json.loads(data.device_data)  # 解析 device_data 字符串为 Python 列表

    return templates.TemplateResponse("index.html", {"request": request, "data": [data] if data else [], "user_id": user_id})
