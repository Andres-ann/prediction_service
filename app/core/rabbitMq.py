import pika
import threading
import logging
import json

from app.core.database import SessionLocal
from app.schemas.sync_schema import ReservationCreate
from app.services.reservations_sinc import DataCollectorService


logger = logging.getLogger(__name__)

def debug_reservation_json(data, db):
    """Debug y mapeo nativo de un objeto ReservationResponseDTO en JSON"""
    try:
        json_data = json.loads(data)
        reservation = ReservationCreate(**json_data)
        print("\n" + "="*50)
        print("📨 MENSAJE RESERVA RECIBIDO (TIPADO)")
        print("="*50)
        print(reservation.model_dump_json(indent=4))
        print("="*50)

        # Guardar en DB (upsert)
        collector = DataCollectorService(db)
        result = collector.store_data(reservation)
        print(f"📌 Resultado DB: {result}")
        return result

    except json.JSONDecodeError as e:
        print(f"❌ Error decodificando JSON: {e}")
        return None
    except Exception as e:
        print(f"❌ Error mapeando al esquema: {e}")
        return None


def callback(ch, method, properties, body):
    db = SessionLocal()
    try:
        json_data = json.loads(body)
        reservation = ReservationCreate(**json_data)
        result = DataCollectorService.store_data(reservation, db)  # <- llamado estático
        print(f"📌 Resultado DB: {result}")
    except Exception as e:
        print(f"❌ Error procesando mensaje: {e}")
    finally:
        db.close()

def start_rabbitmq_consumer():
    """Inicia el consumer de RabbitMQ en un hilo separado"""
    def _consumer_thread():
        try:
            credentials = pika.PlainCredentials(username='admin', password='admin')
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    host='localhost',
                    port=5672,
                    credentials=credentials,
                    virtual_host='/'
                )
            )

            channel = connection.channel()
            channel.queue_declare(queue='reservations', durable=True)

            channel.basic_consume(
                queue='reservations',
                on_message_callback=callback,
                auto_ack=True
            )

            print(' [*] Esperando mensajes JSON de reservas...')
            logger.info(' [*] RabbitMQ Consumer esperando mensajes JSON...')

            channel.start_consuming()

        except Exception as e:
            print(f"❌ Error en RabbitMQ: {e}")
            logger.error(f"Error en RabbitMQ: {e}")

    thread = threading.Thread(target=_consumer_thread, daemon=True)
    thread.start()
    logger.info("✅ RabbitMQ Consumer iniciado en segundo plano")
