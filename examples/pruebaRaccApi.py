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

GENDER, PHOTO, LOCATION, BIO,REPARACIONES,TRAMITES,TAREASHOGAR,FAMILIAYSALUD,ASISTENCIA,RECADOS,MOVILIDAD,MASCOTAS,OCIOYVIAJE,SELECTOR,VOLVER ,SUBREPARACIONES,SUBSUBREPARACIONES,SUBSUBSUBREPARACIONES,BACK,CONTINUAR,INFORMACION,INFORMACION1= range(22)

selecion1=""
selecion2=""
selecion3=""
selecion4=""
email = ""
telefono=""

def start(update, context):
    reply_keyboard = [['Reparaciones', 'Tramites', 'Tareas del hogar'],['Familia y salud',
     'Asistencia', 'Recados'],['Movilidad','Mascotas','Ocio y viajes']]
    user = update.message.from_user
    nom = user.first_name
    logger.info("Gender of %s: %s", nom, update.message.text)

    update.message.reply_text(
         'Soy Nestor y voy a ser su ayudante.'
         'Envia  /cancel para dejar de hablar conmigo.'
         'Que servicio quiere selecionar ?',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    return SELECTOR
    


def selector(update, context):
    reply_keyboard = [['Continuar', 'Volver']]
    user = update.message.from_user
    selecion1 = update.message.text
    logger.info("Gender of %s: %s", user.first_name, update.message.text)
    update.message.reply_text('Usted ha seleccionado')
    update.message.reply_text(update.message.text)
    update.message.reply_text('Introduzca /continuar sino introduzca /volver',reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    if selecion1 == 'Reparaciones' :
        return REPARACIONES

    return VOLVER


def reparaciones(update, context):
    user = update.message.from_user
    reply_keyboard = [['Manitas', 'Cerrajero', 'Electricista','Fontanero'],['Pintor',
     'Carpintero', 'Climatizacion','Persianista'],['Parquetista','Antenista','Albañil','Cristalero'],['Electrodomesticos','Informática','Asistencia mecánica y reparación']]
    logger.info("Gender of %s: %s", user.first_name, update.message.text)
    update.message.reply_text(
         'Seleccione la opcion que usted quiera.\n\n'
         'Envia  /cancel para dejar de hablar conmigo.\n\n'
         'Si quiere volver al inicio pulse /volver',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    return SUBREPARACIONES

   



def subreparaciones(update , context):
    global selecion2
    if(update.message.text != '/back'):
        selecion2 = update.message.text
    logger.info("Last %s", update.message.text)

    if selecion2 == 'Manitas':
        reply_keyboard = [['Reparacion en casa', 'Montaje de TV', 'Montaje de muebles','Otros']]
        update.message.reply_text(
        'Seleccione la opcion que usted quiera .\n\n'
        'Envia  /cancel para dejar de hablar conmigo.\n\n'
        'Envia  /back para volver a elegir el servicio .\n\n',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return SUBSUBREPARACIONES
           

def subsubrepaciones(update , context):
    global selecion3
    if update.message.text != 'Anterior':
        selecion3 = update.message.text

    if selecion3=='Reparacion en casa':
         reply_keyboard = [['2 horas', '3 horas','4 horas']]
         update.message.reply_text(
         'Seleccione cuantas horas nececitara nuestro servicio.\n\n'
         'Envia  /cancel para dejar de hablar conmigo.\n\n'
         'Evia /back para cambiar de servicio.\n\n',
          reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    
    return SUBSUBSUBREPARACIONES
                
def subsubsubreparaciones(update,context):
    reply_keyboard = [['Continuar', 'Volver', 'Cancelar','Anterior']]
    global selecion4
    selecion4 = update.message.text
    if selecion4=='2 horas' or selecion4=='3 horas':
        update.message.reply_text('Precio : 61,71')

    if(selecion4=='4 horas'):
        update.message.reply_text('Precio : 111,08')


    update.message.reply_text(  'Para continuar introducir Continuar \n\n'
                'Para volver al menú  Volver\n\n'
                'Para salir pulse Cancel\n\n'
                'Para cambiar numero de horas pulse Back\n\n',reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    return CONTINUAR 


def informacion(update,context):

    update.message.reply_text(  'Introduca email')
    
    return INFORMACION 

def informacion2(update,context):
    global email 
    email = update.message.text 
    update.message.reply_text('Introduca número de telefono')
    return INFORMACION1


def informacion3(update,context):
    global telefono
    telefono = update.message.text 
    update.message.reply_text('Se le avisara en un máximo de 48 horas la confirmación del servicio')
    return ConversationHandler.END



def photo(update, context):
    user = update.message.from_user
    photo_file = update.message.photo[-1].get_file()
    photo_file.download('user_photo.jpg')
    logger.info("Photo of %s: %s", user.first_name, 'user_photo.jpg')
    update.message.reply_text('Gorgeous! Now, send me your location please, '
                              'or send /skip if you don\'t want to.')

    return LOCATION


def skip_photo(update, context):
    user = update.message.from_user
    logger.info("User %s did not send a photo.", user.first_name)
    update.message.reply_text('I bet you look great! Now, send me your location please, '
                              'or send /skip.')

    return LOCATION


def location(update, context):
    user = update.message.from_user
    user_location = update.message.location
    logger.info("Location of %s: %f / %f", user.first_name, user_location.latitude,
                user_location.longitude)
    update.message.reply_text('Maybe I can visit you sometime! '
                              'At last, tell me something about yourself.')

    return BIO


def skip_location(update, context):
    user = update.message.from_user
    logger.info("User %s did not send a location.", user.first_name)
    update.message.reply_text('You seem a bit paranoid! '
                              'At last, tell me something about yourself.')

    return BIO


def bio(update, context):
    user = update.message.from_user
    logger.info("Bio of %s: %s", user.first_name, update.message.text)
    update.message.reply_text('Gracias! Espero poder hablar de nuevo con usted .')

    return ConversationHandler.END


def cancel(update, context):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text('Adios! Espero poder hablar de nuevo con usted .',
                              reply_markup=ReplyKeyboardRemove())

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
            REPARACIONES: [ MessageHandler(Filters.regex('^(Continuar)$'), reparaciones),
             CommandHandler('reparaciones', reparaciones),CommandHandler('continuar', reparaciones),MessageHandler(Filters.regex('^(Volver)$'),start)],

            TRAMITES: [MessageHandler(Filters.regex('^(Tramites)$'), start)],

            TAREASHOGAR: [ MessageHandler(Filters.regex('^(Tareas del hogar)$'), start)],

            FAMILIAYSALUD: [ MessageHandler(Filters.regex('^(Familia y salud)$'), start)],

            ASISTENCIA: [ MessageHandler(Filters.regex('^(Asistencia)$'), start)],


            RECADOS: [MessageHandler(Filters.regex('^(Continuar)$'), start),
            CommandHandler('recados', start)],


            MOVILIDAD: [ MessageHandler(Filters.regex('^(Movilidad)$'), start)],

            MASCOTAS: [ MessageHandler(Filters.regex('^(Mascotas)$'), start)],


            OCIOYVIAJE: [ MessageHandler(Filters.regex('^(Ocio y viajes)$'), start)],

            SELECTOR:[  CommandHandler('cancel', cancel),MessageHandler(Filters.text, selector)
                   ],
         
            PHOTO: [MessageHandler(Filters.photo, photo),
                    CommandHandler('skip', skip_photo)],

            LOCATION: [MessageHandler(Filters.location, location),
                       CommandHandler('skip', skip_location)],

            BIO: [MessageHandler(Filters.text, bio)],

            VOLVER:[MessageHandler(Filters.regex('^(Volver)$'),start)],

            SUBREPARACIONES:[MessageHandler(Filters.text, subreparaciones),
                            CommandHandler('subreparaciones', subreparaciones)],
                                
            SUBSUBREPARACIONES:[MessageHandler(Filters.regex('^(Reparacion en casa|Montaje de TV|Montaje de muebles|Otros|Anterior)$'), subsubrepaciones),
                            CommandHandler('subsubreparaciones', subsubrepaciones),CommandHandler('back', reparaciones)],

            SUBSUBSUBREPARACIONES:[MessageHandler(Filters.regex('^(2 horas|3 horas|4 horas)$'), subsubsubreparaciones),
                            CommandHandler('skip', start) ,CommandHandler('back', subreparaciones) ],
        
            CONTINUAR: [
            MessageHandler(Filters.regex('^(Continuar)$'), informacion),
            MessageHandler(Filters.regex('^(Anterior)$'),subsubrepaciones),
            MessageHandler(Filters.regex('^(Cancelar)$'),cancel),
            MessageHandler(Filters.regex('^(Volver)$'),start)]
            ,

            INFORMACION:[MessageHandler(Filters.text, informacion2),
                            CommandHandler('skip', start)],

            INFORMACION1:[MessageHandler(Filters.text, informacion3),
                            CommandHandler('skip', start)]

     





        },

        fallbacks=[CommandHandler('cancel', cancel),CommandHandler('volver',start)]
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

