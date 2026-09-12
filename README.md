# 烘鞋器 · 品牌价格看板

46款商品，180条已标价SKU，11个规格暂未标价。按品牌、商品筛选价格段；商品图片点击放大，SKU默认折叠。不统计销量。

## Streamlit Community Cloud 部署

1. 将本目录内容上传到 GitHub 仓库根目录。
2. 登录 https://share.streamlit.io ，选择 Create app → Deploy a public app from GitHub（私有仓库按账户授权选择）。
3. 选择仓库、`main` 分支，入口文件填写 `app.py`。
4. 使用 Python 3.12，点击 Deploy。无需配置密钥。

## 数据更新

`data.json` 存放商品信息、SKU名称和售价；`static/thumbs/` 存放缩略图，`static/full/` 存放点击后加载的原图。更新后提交到 GitHub，Streamlit 将重新部署。

## 已部署用户升级到加速版

1. 解压部署包，将里面的文件和文件夹上传到原 GitHub 仓库根目录，不要只上传 ZIP，也不要多套一层文件夹。
2. 可以分两次上传：先上传整个 `static` 文件夹，再上传其余文件覆盖旧版。务必包含 `.streamlit/config.toml`，它负责开启图片访问。
3. 提交后等待 Streamlit 更新，刷新原来的访问链接即可。入口仍是 `app.py`，不需要新建应用。旧的 `assets` 文件夹可保留，但新版不再使用。

新版将图片移出页面正文，列表使用延迟加载的缩略图，点击放大时才请求原图。页面正文约76 KB；图片仍需另外下载，实际打开速度受网络和云端启动影响。

`skus` 只包含有明确价格的规格；未标价规格放在对应商品的 `unpricedSkus` 中，不计入统计。价格来自用户表格中的SKU截图及红字标注，部分优惠存在条件。截断名称和已知来源差异保留标注。

网页内“补充数据”仅修改当前页面数据，需导出备份；不会自动写回 GitHub。

仓库不包含原始Excel、含个人信息的SKU截图、凭据、电脑IP或部署密钥。商品图片及名称来自用户提供的竞品资料。

## 本地运行

```sh
pip install -r requirements.txt
streamlit run app.py
```
