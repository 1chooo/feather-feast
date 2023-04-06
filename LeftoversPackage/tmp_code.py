# STATUS = ''
        # STATUS = '商家名稱：' + STORE_NAME + '\n'
        # STATUS += '商家地址：' + STORE_ADDRESS + '\n'
        # STATUS += '商品種類數量：' + PRODUCT_TYPE_AMOUNT + '\n'
        # STATUS += '第一項商品資訊：\n'
        # STATUS += '第一項商品名稱：' + FIRST_PRODUCT_NAME + '\n'
        # STATUS += '第一項商品數量：' + FIRST_PRODUCT_AMOUNT + '\n'
        # STATUS += '第一項商品售價：' + FIRST_PRODUCT_PRICE + '\n'
        # STATUS += '第二項商品資訊：\n'
        # STATUS += '第二項商品名稱：' + SECOND_PRODUCT_NAME + '\n'
        # STATUS += '第二項商品數量：' + SECOND_PRODUCT_AMOUNT + '\n'
        # STATUS += '第二項商品售價：' + SECOND_PRODUCT_PRICE + '\n'
        # STATUS += '第三項商品資訊：\n'
        # STATUS += '第三項商品名稱：' + THIRD_PRODUCT_NAME + '\n'
        # STATUS += '第三項商品數量：' + THIRD_PRODUCT_AMOUNT + '\n'
        # STATUS += '第三項商品售價：' + THIRD_PRODUCT_PRICE + '\n'
        # STATUS += '最佳食用期限：' + EXPIRY_DATE + '\n'
        # STATUS += '最後取餐時間：' + PICKUP_TIME + '\n'
        # print(STATUS)

# STATUS = f'商家名稱：{STORE_NAME}\n\
            #            商家地址：{STORE_ADDRESS}\n\
            #            商品種類數量：{PRODUCT_TYPE_AMOUNT}\n\
            #            第一項商品資訊：\n\
            #            第一項商品名稱：{FIRST_PRODUCT_NAME}\n\
            #            第一項商品數量：{FIRST_PRODUCT_AMOUNT}\n\
            #            第一項商品售價：{FIRST_PRODUCT_PRICE}\n\
            #            第二項商品資訊：\n\
            #            第二項商品名稱：{SECOND_PRODUCT_NAME}\n\
            #            第二項商品數量：{SECOND_PRODUCT_AMOUNT}\n\
            #            第二項商品售價：{SECOND_PRODUCT_PRICE}\n\
            #            第三項商品資訊：\n\
            #            第三項商品名稱：{THIRD_PRODUCT_NAME}\n\
            #            第三項商品數量：{THIRD_PRODUCT_AMOUNT}\n\
            #            第三項商品售價：{THIRD_PRODUCT_PRICE}\n\
            #            最佳食用期限：{EXPIRY_DATE}\n\
            #            最後取餐時間：{PICKUP_TIME}\n'

""" __message words limits__
                if happened, use the below comment code.
            """
            # message2 = TextSendMessage(
            #     text='第一項商品資訊：\n' +
            #     '第一項商品名稱：' + FIRST_PRODUCT_NAME + '\n' +
            #     '第一項商品數量：' + str(FIRST_PRODUCT_AMOUNT) + '\n' +
            #     '第一項商品售價：' + str(FIRST_PRODUCT_PRICE))
            # reply_message.append(message2)
            # message3 = TextSendMessage(
            #     text='第二項商品資訊：\n' +
            #     '第二項商品名稱' + SECOND_PRODUCT_NAME + '\n' +
            #     '第二項商品數量' + str(SECOND_PRODUCT_AMOUNT) + '\n' +
            #     '第二項商品售價' + str(SECOND_PRODUCT_PRICE))
            # reply_message.append(message3)
            # message4 = TextSendMessage(
            #     text='第三項商品資訊：\n' +
            #     '第三項商品名稱' + THIRD_PRODUCT_NAME + '\n' +
            #     '第三項商品數量' + str(THIRD_PRODUCT_AMOUNT) + '\n' +
            #     '第三項商品售價' + str(THIRD_PRODUCT_PRICE) + '\n')
            # reply_message.append(message4)


if READY_TO_GET_FIRST_PRODUCT_IMAGE == True:

        reply_message = []

        message1 = TextSendMessage(
            text='第一種商品照片已成功上傳，上傳時間： ' + 
            str(datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")))
        reply_message.append(message1)
        reply_message.append(
            Generator.image_upload_carousel)
        message2 = TextSendMessage(
            text='請繼續點擊「第二種商品照片」按鈕以繼續上傳，' +
            '若無後續圖片需要上傳請點選下方「我已上傳完成」按鈕')
        reply_message.append(message2)
        reply_message.append(
            Generator.no_more_image_quick_reply)

        line_bot_api.reply_message(
            event.reply_token,
            reply_message)

        # 下載照片
        try:
            message_content = line_bot_api.get_message_content(event.message.id)

            output_path = './uploader/' + current_date +\
                '_' + STORE_NAME + \
                '_' + FIRST_PRODUCT_NAME + '.jpg'

            with open(output_path, 'wb') as fd:
                for chunk in message_content.iter_content():
                    fd.write(chunk)

        except LineBotApiError as e:
            # 如果發生例外，記錄錯誤訊息
            print('Unable to get message content: ' + str(e))

    elif READY_TO_GET_SECOND_PRODUCT_IMAGE == True:

        reply_message = []

        message1 = TextSendMessage(
            text='第二種商品照片已成功上傳，上傳時間： ' + 
            str(datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")))
        reply_message.append(message1)
        reply_message.append(
            Generator.image_upload_carousel)
        message2 = TextSendMessage(
            text='請繼續點擊「第三種商品照片」按鈕以繼續上傳，' +
            '若無後續圖片需要上傳請點選下方「我已上傳完成」按鈕')
        reply_message.append(message2)
        reply_message.append(
            Generator.no_more_image_quick_reply)

        line_bot_api.reply_message(
            event.reply_token,
            reply_message)

        # 下載照片
        try:
            message_content = line_bot_api.get_message_content(event.message.id)

            output_path = './uploader/' + current_date +\
                '_' + STORE_NAME + \
                '_' + SECOND_PRODUCT_NAME + '.jpg'

            with open(output_path, 'wb') as fd:
                for chunk in message_content.iter_content():
                    fd.write(chunk)

        except LineBotApiError as e:
            # 如果發生例外，記錄錯誤訊息
            print('Unable to get message content: ' + str(e))

    elif READY_TO_GET_THIRD_PRODUCT_IMAGE == True:

        reply_message = []

        message1 = TextSendMessage(
            text='第三種商品照片已成功上傳，上傳時間： ' + 
            str(datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")))
        reply_message.append(message1)
        reply_message.append(
            Generator.image_upload_carousel)
        message2 = TextSendMessage(
            text='若已完成上傳請幫我點擊下方確認按鈕')
        reply_message.append(message2)
        reply_message.append(
            Generator.check_image_quick_reply)

        line_bot_api.reply_message(
            event.reply_token,
            reply_message)

        # 下載照片
        try:
            message_content = line_bot_api.get_message_content(event.message.id)

            output_path = './uploader/' + current_date +\
                '_' + STORE_NAME + \
                '_' + SECOND_PRODUCT_NAME + '.jpg'

            with open(output_path, 'wb') as fd:
                for chunk in message_content.iter_content():
                    fd.write(chunk)

        except LineBotApiError as e:
            # 如果發生例外，記錄錯誤訊息
            print('Unable to get message content: ' + str(e))