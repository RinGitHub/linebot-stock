在程式碼中，即時股價及歷史股價線圖的實做是參考了Github上的程式碼，在依需求做變更。
由於此機器人依使用者輸入訊息的首字母做為功能判別，
因此首先在取得使用者訊息後，以if-else判斷首字母為和，來做功能分類。

1. 若首字母為P，表示目前使用者想查詢即時股價，在P這個區塊的程式碼中，首先截取P後方的股號存入變數Text，再利用twstock中realtime的即時查股API取得即時股價，為避免主程式過於龐大，用p_success這個function來包查詢即時股價的細部功能，並將return設為回傳訊息內容；
若使用者輸入的是無效股號，則會判定為KeyError，將回傳訊息設為提醒使用者須重新輸入，最後再將content及本次接收訊息的event傳入send_text_message這個function完成訊息傳送。

p_success及send_text_message的作用：
p_success的目的是將從twstock取得該股號的即時股價整理並格式化成所要的格式再把這些文字包在content中回傳。
send_text_message的作用就是在傳輸文字，包含三個屬性：token、訊息的形式及訊息中的文字，由於傳送文字訊息的功能會被多次使用，所以也將它包成funtion。

2. 若首字母為K，表示目前使用者想查詢歷史股價線圖，跟查詢即時股價很類似，只是這次是用stock來取得歷史股價資料，處理例外的狀況和上個功能相同，但由於這次成功時迴傳的是圖片訊息，失敗時回傳文字訊息，因此在傳訊息時格式不相同。
成功時的k_success function的作用，首先用pandas的DataFrame物件將歷史股價整理成像是表格的結構，再利用Matplotlib將資料視覺化，最後將資料上傳用upload_image function上傳至imageer，並取得圖片網址後，將圖片訊息傳給使用者。

3. 若首字母為F，表示目前使用者想查詢公司基本資訊及基本面，由於用twstock判斷是否為有效股號較快，因此雖然此功能並不會用到twstock查詢股價，還是利用其來做為有效股號的判別。
f_success funtion的作用，在這個function中開始又會呼叫另一個function，這個function的目的是要獲得公司基本資訊，在這個function中，我們利用股號去goodinfo網站爬取該股號的相關頁面，首先取得股票代碼及公司名稱，由於Goodinfo的網頁資訊煩雜，因此直接以抓取關鍵字"產業別"的方式取得所要的資訊，遇到的一個狀況是有該公司的網頁，但沒有公司基本資料，所以這邊放了一個提醒告知使用者，若能正確取得資訊後將其整理並放到content中return。
回到f_success，這邊又放了一個判斷是因為goodinfo即使是無該股號的頁面也會有正常的網頁，但因為爬不到任何東西所以content會是空的，若其為空則提醒使用者。若goodinfo這邊的取得資訊都正常，那就將content包回覆的list中，因為這個功能一次要回傳兩個訊息，
接下來是第二個訊息，因為這個訊息是將tradingview上的基本面資訊截圖，所以先設定開啟瀏覽器時的各項設定，再去網站爬取所要的物件，但這個網站並非所有股號都有相關的基本面資訊，所以當無相關資訊時，直接終止並回傳訊息提醒使用者，若有相關資訊，則可順利找到該表表格先整頁截圖後，再依劇表格位置截取該區塊，並將圖片上傳至imager後將圖片網址也放入回傳訊息的list中，最後將整個list回傳給使用者。

4. 若首字母為D，表示使用者想查詢殖利率推薦標的。
d_success function的作用，在這個功能中我們會去撿骨讚網站爬取股號、公司名稱、股價、殖利率，並根據使用者輸入的資金預算及殖利率，找到符合條件且殖利率最高的前五個標的，若該條件都無法找到任何標第，則將回傳訊息設為提醒使用者，最後不論是否成功取得標的都return content後將訊息回傳完成標的推薦。

5. 最後是若使用者輸入的訊息非上述開頭字母或幫助，則回傳訊息提醒使用者。
