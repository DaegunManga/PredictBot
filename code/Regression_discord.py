import discord #이 버전은 1.7.3 버전으로 작성되었음.
import Regression_py as rp
from discord.ext import commands
import Regression2_py as rp2
from discord.ui import Button, View
import config

client = commands.Bot(command_prefix='/',intents=discord.Intents.all())


f = rp.Regression_f()
f2 = rp2.Regression2_f()
f2.load_data()
f2.pred_Prophet()

@client.event #다음으로, Client의 인스턴스를 만듭니다. 이 클라이언트는 디스코드로의 연결입니다.
async def on_ready(): #그러고 Client.event() 데코레이터를 사용해서 이벤트를 등록합니다. 이 라이브러리에는 많은 이벤트들이 있습니다. 이 라이브러리는 비동기이기 때문에, 우리는 《callback》 스타일로 합니다.
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    # if message.author == client.user: #봇이 보낸 메세지 무시
        # return
    if message.content.startswith('hello'):
        await message.channel.send('Hello!')

    if message.content.startswith('새로고침'):
        await message.channel.send('Ok wait a Minute Please!')
        f2.load_data()
        f2.pred_Prophet()


    if message.content.startswith("예측") :
        button1 = Button(label = "Sklearn", style = discord.ButtonStyle.green)
        button2 = Button(label = "Prophet", style = discord.ButtonStyle.green)

        async def button_callback(interacton) :
            await interacton.response.send_message("Let's Go!")
            in_num, train_num, test_num = f.return_info()
            a1, a2, a3, a4, a5 = f.LinearRegressionf()
            Poly_L = list(f.polyRegressionf())
            await message.channel.send('----------------------------------')
            await message.channel.send("입력받은 데이터의 총 개수 : " + str(in_num))
            await message.channel.send("훈련 할 총 데이터의 개수 : " + str(train_num))
            await message.channel.send("테스트 할 총 데이터의 개수 : " + str(test_num))
            await message.channel.send('----------------------------------')

            image = discord.File("./../fig/Linear_fig.png", filename="Linear_fig.png")
            await message.channel.send(file=image)
            embed=discord.Embed(title="LinearRegression 점수", color=0x05ff09)
            embed.set_author(name="Made by. MANGA - AI Department", url="https://github.com/MINO-LOVER", icon_url="https://avatars.githubusercontent.com/u/69490709?s=400&u=0c1c589130bd156f0e591f43f320bf9511e24ded&v=4")
            embed.add_field(name="MAE", value=round(a1), inline=True)
            embed.add_field(name="MSE", value=round(a3), inline=True)
            embed.add_field(name="RMSE", value=round(a2), inline=False)
            embed.add_field(name="Rsuqare", value=round(a4), inline=True)
            await message.channel.send(embed=embed)

            image = discord.File("./../fig/poly_fig.png", filename="poly_fig.png")
            await message.channel.send(file=image)
            embed=discord.Embed(title="PolyNomialRegression 점수", color=0x05ff09)
            embed.set_author(name="Made by. MANGA - AI Department", url="https://github.com/MINO-LOVER", icon_url="https://avatars.githubusercontent.com/u/69490709?s=400&u=0c1c589130bd156f0e591f43f320bf9511e24ded&v=4")
            embed.add_field(name="MAE", value=round(Poly_L[0]), inline=True)
            embed.add_field(name="MSE", value=round(Poly_L[1]), inline=True)
            embed.add_field(name="RMSE", value=round(Poly_L[2]), inline=False)
            embed.add_field(name="Rsuqare", value=round(Poly_L[3]), inline=True)
            await message.channel.send(embed=embed)

            Lin_pred, Poly_pred = f.return_predict()
            await message.channel.send("Linear Regression 기준 : " + str(Lin_pred) + "명,  점수 : " + str(a5))
            await message.channel.send("Polynomial Regression 기준 : " + str(Poly_pred) + "명,  점수 : " + str(Poly_L[4]))
    

        
        async def button2_callback(interacton) :
            await interacton.response.send_message("Let's Go!")
            image = discord.File("./../fig/Prophet_fig.png", filename="Linear_fig.png")
            await message.channel.send(file=image)

            button1 = Button(label = "More(With Event, Trend)", style = discord.ButtonStyle.green)
            button2 = Button(label = "Detail", style = discord.ButtonStyle.green)
            df_future = f2.return_info()
            for y in range (6, -1, -1) :
                await message.channel.send(str(df_future.loc[max(df_future.index)- y, "ds"])[0 : 10] + ' : ' + str(df_future.loc[max(df_future.index)-y, "yhat"]) + "명")

            async def button_callback(interacton) :
                image = discord.File("./../fig/change_point_fig.png", filename="change_point_fig.png")
                await interacton.response.send_message(file=image)

            async def button2_callback(interacton) :
                image = discord.File("./../fig/detail_fig.png", filename="detail_fig.png")
                await interacton.response.send_message(file=image)

            button1.callback = button_callback
            button2.callback = button2_callback
            view = View()
            view.add_item(button1)
            view.add_item(button2)
            await message.channel.send("추가 정보" , view = view)
            await client.wait_for("button_click")

        
        button1.callback = button_callback
        button2.callback = button2_callback
        view = View()
        view.add_item(button1)
        view.add_item(button2)
        await message.channel.send("사용할 모듈을 정해주세요." , view = view)
        await client.wait_for("button_click")

client.run(config.dis_api_key)