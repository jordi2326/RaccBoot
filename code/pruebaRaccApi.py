#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.

"""
First, a few callback functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Example of a bot-user conversation using ConversationHandler.
Send /start to initiate the conversation.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging

from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler)

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

GENDER, PHOTO, LOCATION, LOCATIONMANUAL, BIO, REPARACIONES, TRAMITES, TAREASHOGAR, FAMILIAYSALUD, ASISTENCIA, RECADOS, MOVILIDAD, MASCOTAS, OCIOYVIAJE, SELECTOR, VOLVER, SUBREPARACIONES, SUBSUBREPARACIONES, SUBSUBSUBREPARACIONES, BACK, CONTINUAR, INFORMACION, INFORMACION1, PAGAR, FECHA = range(
    25)

selecion1 = ""
selecion2 = ""
selecion3 = ""
selecion4 = ""
email = ""
telefono = ""
detected_address = ""
detected_address_extra = ""
presupuesto = 0


def start(update, context):
    reply_keyboard = [['Reparaciones', 'Tramites', 'Tareas del hogar'], ['Familia y salud',
                                                                         'Asistencia', 'Recados'],
                      ['Movilidad', 'Mascotas', 'Ocio y viajes']]
    user = update.message.from_user
    nom = user.first_name
    logger.info("%s: %s", nom, update.message.text)

    update.message.reply_text(
        '¡Bienvenido! Soy Nestor y voy a ser tu asistente personal.\n\n'
        'Pídeme lo que quieras y disfruta de tu tiempo para las cosas que realmente importan.\n'
        'Reserva tu servicio en pocos pasos y obtén un presupuesto al momento.\n'
        'Puedes enviar "/cancel" en cualquier momento para dejar de hablar conmigo.\n\n'
        '¿Que servicio necesitas?\n',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    return SELECTOR


def selector(update, context):
    reply_keyboard = [['Continuar', 'Volver']]
    user = update.message.from_user
    selecion1 = update.message.text
    logger.info("%s: %s", user.first_name, update.message.text)
    update.message.reply_text("Has seleccionado: " + str(selecion1))
    # update.message.reply_text(update.message.text)
    update.message.reply_text('Introduzca /continuar si no introduzca /volver',
                              reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    if selecion1 == 'Reparaciones':
        return REPARACIONES

    return VOLVER


def reparaciones(update, context):
    user = update.message.from_user
    reply_keyboard = [['Manitas', 'Cerrajero', 'Electricista', 'Fontanero'],
                      ['Pintor', 'Carpintero', 'Climatización', 'Persianista'],
                      ['Parquetista', 'Antenista', 'Albañil', 'Cristalero'],
                      ['Electrodomésticos', 'Informática', 'Asistencia mecánica y reparación']]
    logger.info("%s: %s", user.first_name, update.message.text)
    update.message.reply_text(
        '¿Que tipo de reparaciones necesitas?\n\n'
        'Selecciona la opción que quieras.\n\n'
        'Envía /cancel para dejar de hablar conmigo.\n\n'
        'Si quieres volver al inicio pulsa /volver',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    return SUBREPARACIONES


def subreparaciones(update, context):
    global selecion2
    if (update.message.text != '/back'):
        selecion2 = update.message.text
    logger.info("Last %s", update.message.text)
    update.message.reply_text("Has seleccionado: " + str(selecion2))
    if selecion2 == 'Manitas':
        reply_keyboard = [['Reparación en casa', 'Montaje de TV'],['Montaje de muebles', 'Otros']]
        update.message.reply_text(
            '¡Dinos que necesitas y nos encargamos de todo!\n'
            'Manitas verificados de confianza.\n'
            'Garantía de 6 meses.\n'
            'Desplazamiento incluido.\n\n'
            'Selecciona la opción que quieras.\n\n'
            'Envía /cancel para dejar de hablar conmigo.\n\n'
            'Envía /back para volver a elegir el servicio.\n\n',
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return SUBSUBREPARACIONES


def subsubrepaciones(update, context):
    global selecion3
    if update.message.text != 'Back':
        selecion3 = update.message.text

    if selecion3 == 'Reparación en casa':
        reply_keyboard = [['2 horas', '3 horas', '4 horas']]
        update.message.reply_text(
            'Indica el numero de horas que más se adapte a tus necesidades.\n\n'
            'Envía /cancel para dejar de hablar conmigo.\n\n'
            'Envía /back para cambiar de servicio.\n\n',
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    return SUBSUBSUBREPARACIONES


def subsubsubreparaciones(update, context):
    reply_keyboard = [['Continuar', 'Volver'],['Cancelar', 'Anterior']]
    global selecion4
    global presupuesto
    selecion4 = update.message.text
    if selecion4 == '2 horas' or selecion4 == '3 horas':
        update.message.reply_text('Precio : 61,71 €')
        presupuesto = 61.71

    if (selecion4 == '4 horas'):
        update.message.reply_text('Precio : 111,08 €')
        presupuesto = 111.08

    update.message.reply_text('Para continuar introducir Continuar \n\n'
                              'Para volver al menú Volver\n\n'
                              'Para salir pulsa Cancel\n\n'
                              'Para cambiar el numero de horas pulsa Back\n\n',
                              reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    return CONTINUAR


def informacion(update, context):
    update.message.reply_text('Introduzca correo electrónico')

    return INFORMACION


def informacion2(update, context):
    global email
    email = update.message.text
    # Enviar correo en 2o plano background
    receiver_email = email  # Enter receiver address
    import threading
    download_thread = threading.Thread(target=enviarCorreo, args=[receiver_email])
    download_thread.start()
    update.message.reply_text('Presupuesto enviado por correo. Introduzca número de teléfono')
    return INFORMACION1


def informacion3(update, context):
    global telefono
    telefono = update.message.text
    update.message.reply_text('Envíe fotos para más detalles o /skip para omitir')

    return PHOTO


def photo(update, context):
    user = update.message.from_user
    photo_file = update.message.photo[-1].get_file()
    photo_file.download('user_photo.jpg')
    logger.info("Photo of %s: %s", user.first_name, 'user_photo.jpg')
    update.message.reply_text('Introduzca su ubicación o /skip para omitir')

    return LOCATION


def location(update, context):
    global detected_address
    user = update.message.from_user
    user_location = update.message.location
    logger.info("Location of %s: %f / %f", user.first_name, user_location.latitude,
                user_location.longitude)
    url = "https://maps.googleapis.com/maps/api/geocode/json?latlng=" + str(user_location.latitude) + "," + str(
        user_location.longitude) + "&key=AIzaSyCdBzOsXA50MuzG8-xLz9C9LTnlBr2LiQc"
    import requests, json, urllib3
    logger.info(url)
    response = requests.get(url).json()
    logger.info(response)
    logger.info(response["results"][0]["formatted_address"])
    detected_address = response["results"][0]["formatted_address"]
    update.message.reply_text("Hemos detectado la ubicacion seguiente: ")
    update.message.reply_text(str(detected_address))
    update.message.reply_text("Ahora agrega mas informacion como el numero de piso. Para saltar este paso introduce /skip")

    return LOCATIONMANUAL
# location, location manual, skip locationman, skip location, 22-23, func declaration, global
def location_manual(update, context):
    global detected_address_extra
    detected_address_extra = update.message.text
    update.message.reply_text("Introduce el dia cuando usted quiere que nos pasemos en formato dd/mm/aaaa. Para saltar este paso introduce /skip")
    return FECHA

def skip_location_manual(update, context):
    update.message.reply_text("Introduce el dia cuando usted quiere que nos pasemos en formato dd/mm/aaaa. Para saltar este paso introduce /skip")
    return FECHA

def skip_location(update, context):
    update.message.reply_text("Introduce el dia cuando usted quiere que nos pasemos en formato dd/mm/aaaa. Para saltar este paso introduce /skip")
    return FECHA

def fecha(update, context):
    update.message.reply_text('Para pagar introduzca la tarjeta bancaria en formato [numero],[mes],[anyo],[cvc]. Por ejemplo 4242424242424242,6,2021,314\nO introduzca /skip para omitir y pagar en efectivo')
    return PAGAR

def skip_fecha(update, context):
    update.message.reply_text('Para pagar introduzca la tarjeta bancaria en formato [numero],[mes],[anyo],[cvc]. Por ejemplo 4242424242424242,6,2021,314\nO introduzca /skip para omitir y pagar en efectivo')
    return PAGAR



def introloc(update, context):
    update.message.reply_text('Introduzca su ubicación o /skip para omitir')

    return LOCATION



def bio(update, context):
    user = update.message.from_user
    logger.info("Bio of %s: %s", user.first_name, update.message.text)
    update.message.reply_text('¡Gracias! Espero poder hablar de nuevo con usted.')

    return ConversationHandler.END


def enviarCorreo(receiver_email):
    import email, smtplib, ssl
    from email import encoders
    from email.mime.base import MIMEBase
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart

    # port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = "PAEQ22020@gmail.com"  # Enter your address
    # password = input("Type your password and press enter: ")
    password = "botracc2020"

    message = MIMEMultipart("alternative")
    message["Subject"] = "Presupuesto manitas"
    message["From"] = "Bot RACC"
    message["To"] = receiver_email

    # Create the plain-text and HTML version of your message
    text = """\
    Hola,
    Adjuntamos el presupuesto de los servicios que ha solicitado.
    Muchas gracias por su confianza.

    Atentamente,
    RACC"""
    html = """\
    <html>
      <body>
        <p>Hola,<br>
           Adjuntamos el presupuesto de los servicios que ha solicitado.<br>
           Muchas gracias por su confianza.<br>
           <br>
           Atentamente,<br>
           RACC
        </p>
      </body>
    </html>
    """

    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)
    message.attach(part2)

    filename = "Presupuesto.pdf"  # In same directory as script

    # Open PDF file in binary mode
    with open(filename, "rb") as attachment:
        # Add file as application/octet-stream
        # Email client can usually download this automatically as attachment
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

    # Encode file in ASCII characters to send by email
    encoders.encode_base64(part)

    # Add header as key/value pair to attachment part
    part.add_header(
        "Content-Disposition",
        "attachment; filename= {filename}",
    )

    # Add attachment to message and convert message to string
    message.attach(part)

    # Create a secure SSL context
    context = ssl.create_default_context()
    server = smtplib.SMTP_SSL(smtp_server)
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, message.as_string())
    server.quit()


def cancel(update, context):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text('¡Adiós! Espero poder hablar de nuevo con usted.',
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


def pagar(update, context):
    # para testear: 4242424242424242,6,2021,314
    if(update.message.text == "/skip"):  return skip_pagar(update, context)
    tarjeta_info = update.message.text.split(",")
    import stripe
    stripe.api_key = "sk_test_51GtXF4Cpb85sHqrBKXCKSmG1BWAPeHiZLEsx9cPIpbjFF2YmhaJgeT5Ynt71pQPG6MvkTcLFSFcsFMH755pqhXkK00eRFJVb17"
    global presupuesto
    charge = stripe.Charge.create(
        amount=int(presupuesto * 100),
        currency="eur",
        description="My First Test Charge (created for API docs)",
        source=stripe.Token.create(
            card={
                "number": tarjeta_info[0],
                "exp_month": int(tarjeta_info[1]),
                "exp_year": int(tarjeta_info[2]),
                "cvc": tarjeta_info[3],
            },
        ),
    )
    return skip_pagar(update, context)


def skip_pagar(update, context):
    user = update.message.from_user
    update.message.reply_text('¡Gracias! Espero poder hablar de nuevo con usted.')

    return ConversationHandler.END

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater("1197852167:AAETya5xtPT06hjp8VJQxbZQuL5M7Fk8h8k", use_context=True)


    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            REPARACIONES: [MessageHandler(Filters.regex('^(Continuar)$'), reparaciones),
                           CommandHandler('reparaciones', reparaciones), CommandHandler('continuar', reparaciones),
                           MessageHandler(Filters.regex('^(Volver)$'), start)],

            TRAMITES: [MessageHandler(Filters.regex('^(Tramites)$'), start)],

            TAREASHOGAR: [MessageHandler(Filters.regex('^(Tareas del hogar)$'), start)],

            FAMILIAYSALUD: [MessageHandler(Filters.regex('^(Familia y salud)$'), start)],

            ASISTENCIA: [MessageHandler(Filters.regex('^(Asistencia)$'), start)],

            RECADOS: [MessageHandler(Filters.regex('^(Continuar)$'), start),
                      CommandHandler('recados', start)],

            MOVILIDAD: [MessageHandler(Filters.regex('^(Movilidad)$'), start)],

            MASCOTAS: [MessageHandler(Filters.regex('^(Mascotas)$'), start)],

            OCIOYVIAJE: [MessageHandler(Filters.regex('^(Ocio y viajes)$'), start)],

            SELECTOR: [CommandHandler('cancel', cancel),
                       MessageHandler(Filters.regex('^(Reparaciones)$'), reparaciones)],

            PHOTO: [MessageHandler(Filters.photo, photo),
                    CommandHandler('skip', introloc)],

            LOCATION: [MessageHandler(Filters.location, location),
                       CommandHandler('skip', skip_location)],

            LOCATIONMANUAL: [MessageHandler(Filters.text, location_manual),
                             CommandHandler('skip', skip_location_manual)],

            FECHA: [MessageHandler(Filters.text, fecha),
                    CommandHandler('skip', skip_fecha)],

            BIO: [MessageHandler(Filters.text, bio)],

            VOLVER: [MessageHandler(Filters.regex('^(Volver)$'), start)],

            SUBREPARACIONES: [MessageHandler(Filters.text, subreparaciones),
                              CommandHandler('subreparaciones', subreparaciones)],

            SUBSUBREPARACIONES: [
                MessageHandler(Filters.regex('^(Reparación en casa|Montaje de TV|Montaje de muebles|Otros|Anterior)$'),
                               subsubrepaciones),
                CommandHandler('subsubreparaciones', subsubrepaciones), CommandHandler('back', reparaciones)],

            SUBSUBSUBREPARACIONES: [MessageHandler(Filters.regex('^(2 horas|3 horas|4 horas)$'), subsubsubreparaciones),
                                    CommandHandler('skip', start), CommandHandler('back', subreparaciones)],

            CONTINUAR: [
                MessageHandler(Filters.regex('^(Continuar)$'), informacion),
                MessageHandler(Filters.regex('^(Back)$'), subsubrepaciones),
                MessageHandler(Filters.regex('^(Cancelar)$'), cancel),
                MessageHandler(Filters.regex('^(Volver)$'), start)]
            ,

            PAGAR: [MessageHandler(Filters.text, pagar),
                    CommandHandler('skip', bio)],

            INFORMACION: [MessageHandler(Filters.text, informacion2),
                          CommandHandler('skip', start)],

            INFORMACION1: [MessageHandler(Filters.text, informacion3),
                           CommandHandler('skip', start)]

        },

        fallbacks=[CommandHandler('cancel', cancel), CommandHandler('volver', start)]
    )

    dp.add_handler(conv_handler)

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
