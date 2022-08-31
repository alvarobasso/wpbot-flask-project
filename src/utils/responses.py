class BotResponses:
    
    def responses(type: str) -> str:
        responses = [
            {
                'type': 'success',
                'message': 'La distacia de tu envío es: {}.\nEl tiempo aproximado de entrega es: {}.\nEl costo será de: ${} pesos.\n'
                'Para confirmar tu envío, escribe "confirmar" o escribe "cancelar" para cerrar esa cotización.'
            },
            {
                'type': 'error',
                'message': 'Hola {}, no se pudo calcular el costo, envia nuevamente '
                'la ubicación'
            },
            {
                'type': 'no_shipping_location',
                'message': 'Envia la ubicación de destino de tu paquete para calcular el costo de entrega.'
            },
            {
                'type': 'no_origin_location',
                'message': 'Bienvenido al cotizador de Devolada, por favor ingresa primero la ubicación donde debemos recoger tu paquete.'
            },
            {
                'type': 'save_origin_location',
                'message': 'Gracias ahora envía la ubicación a donde quieres mandar tu paquete.'
            },
            {
                'type': 'error_save_origin_location',
                'message': 'Hubo un problema al registrar tu ubicación de origen, por favor intenta nuevamente.'
            },
            {
                'type': 'error_save_shipping_location',
                'message': 'Hubo un problema al registrar la ubicación de envío, por favor intenta nuevamente.'
            },
            {
                'type': 'error_updating_quote',
                'message': 'Hubo un problema al actualizar la cotización, por favor intenta nuevamente.'
            },
            {
                'type': 'success_closing_quote',
                'message': 'Su cotización se ha cerrado, gracias.'
            },
            {
                'type': 'success_confirming_quote',
                'message': 'Su cotización se ha confirmado, en breve nos comunicaremos contigo para detallar tu servicio, gracias.'
            },
            {
                'type': 'pendding_quoted',
                'message': 'Tienes una cotización pendiente, escribe "cancelar" para cerrar esa cotización o "confirmar" para aceptar el servicio.'
            },
            {
                'type': 'particular_quoted_first_part',
                'message': 'El número {} ha solicitado una cotización desde esta ubicación...'
            },
            {
                'type': 'particular_quoted_second_part',
                'message': 'A esta ubicación. {}'
            },
        ]
        for x in responses:
            if x['type'] == type:
                return x['message']