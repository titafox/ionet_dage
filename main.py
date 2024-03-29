from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Request, Query,Header
from fastapi.templating import Jinja2Templates
from sqlmodel import SQLModel, Field, create_engine, Session
from typing import List
import json
from datetime import datetime

app = FastAPI()

# 添加 CORS 中间件，只允许特定的来源
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://cloud.io.net"],  # 只允许来自 cloud.io.net 的请求，你还得加个你自己的域名
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
            return {"message": "Data received and stored", "data": data}
        else:
            # 如果已存在，不进行插入操作
            return {"message": "Data with the same User-ID and Timestamp already exists", "data": data}


def format_timestamp(value):
    timestamp = int(value) / 1000  # 将毫秒转换为秒
    return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")


templates.env.filters["format_timestamp"] = format_timestamp


def parse_device_data(value):
    print(value)
    return value


templates.env.filters["parse_device_data"] = parse_device_data


# 在后端路由中解析 device_data
@app.get("/", response_model=List[Data])
async def root(request: Request, user_id: str = Query(None)):
    with Session(engine) as session:
        if user_id:
            data = session.query(Data).filter(Data.user_id == user_id).all()
        else:
            data = []
    for item in data:
        item.device_data = json.loads(item.device_data)  # 解析 device_data 字符串为 Python 列表
    return templates.TemplateResponse("index.html", {"request": request, "data": data, "user_id": user_id})
