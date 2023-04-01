def carousel_template_generator_one(
        alt_text, image_url, title, description, 
        label1, label1_info, label2, label2_info,
        label3, label3_info, label4, label4_info,) -> 'TemplateSendMessage':
    
    carousel_template_message = TemplateSendMessage(
        alt_text=alt_text,
        template=CarouselTemplate(
            columns=[
                CarouselColumn(
                    thumbnail_image_url=image_url,
                    title=title,
                    text=description,
                    actions=[
                        MessageAction(
                            label=label1,
                            text=label1_info,
                        ),
                        MessageAction(
                            label=label2,
                            text=label2_info,
                        ),
                        MessageAction(
                            label=label3,
                            text=label3_info,
                        ),
                        MessageAction(
                            label=label4,
                            text=label4_info,
                        ),
                    ]
                ),
            ]
        )
    )
    return carousel_template_message