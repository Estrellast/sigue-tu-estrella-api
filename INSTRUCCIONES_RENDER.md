# 🚀 Desplegar API en Render

## Paso 1: Crear cuenta en Render

1. Ve a: https://render.com
2. Haz clic en **"Get Started"** o **"Sign Up"**
3. Regístrate con tu cuenta de GitHub (recomendado) o email

## Paso 2: Conectar tu repositorio de GitHub

1. Una vez dentro de Render, haz clic en **"New +"** → **"Web Service"**
2. Conecta tu cuenta de GitHub si aún no lo has hecho
3. Busca y selecciona el repositorio: **`Estrellast/sigue-tu-estrella-api`**
4. Haz clic en **"Connect"**

## Paso 3: Configurar el servicio

Render detectará automáticamente que es una aplicación Python. Configura lo siguiente:

### Configuración básica:
- **Name**: `sigue-tu-estrella-api` (o el nombre que prefieras)
- **Region**: Selecciona la más cercana (Europe - Frankfurt o Paris)
- **Branch**: `main`
- **Root Directory**: (déjalo vacío)

### Build & Deploy:
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn app:app --bind 0.0.0.0:$PORT`

### Plan:
- Selecciona **"Free"** (gratis, perfecto para empezar)
  - ⚠️ Nota: El plan gratuito se "duerme" después de 15 minutos de inactividad
  - La primera petición después de dormir tardará ~30 segundos

## Paso 4: Variables de entorno (opcional)

Si necesitas agregar variables de entorno:
1. En la sección **"Environment Variables"**
2. Agrega las que necesites (por ahora no son necesarias)

## Paso 5: Desplegar

1. Haz clic en **"Create Web Service"**
2. Render comenzará a construir y desplegar tu aplicación
3. Verás los logs en tiempo real
4. Espera a que aparezca: **"Your service is live 🎉"**

## Paso 6: Obtener la URL de tu API

Una vez desplegado, Render te dará una URL como:
```
https://sigue-tu-estrella-api.onrender.com
```

Esta es la URL que usarás en tu plugin de WordPress.

## Paso 7: Probar la API

Puedes probar que funciona visitando:
```
https://tu-url.onrender.com/
```

Deberías ver el formulario de cálculo astrológico.

## Paso 8: Actualizar el plugin de WordPress

Edita el archivo del plugin y reemplaza la URL de la API:
```php
$api_url = 'https://tu-url.onrender.com/api/calculate';
```

## 🔄 Actualizaciones automáticas

¡Lo mejor de Render! Cada vez que hagas `git push` a GitHub:
- Render detectará los cambios automáticamente
- Reconstruirá y redesplegarátu aplicación
- Sin necesidad de hacer nada manualmente

## 📊 Monitoreo

En el dashboard de Render podrás ver:
- Logs en tiempo real
- Métricas de uso
- Estado del servicio
- Historial de despliegues

## ⚠️ Limitaciones del plan gratuito

- 750 horas/mes de uso (suficiente para un sitio personal)
- Se "duerme" después de 15 min de inactividad
- 512 MB de RAM
- CPU compartida

## 💡 Consejos

1. **Mantén el servicio activo**: Si quieres evitar que se duerma, puedes usar servicios como UptimeRobot para hacer ping cada 10 minutos
2. **Revisa los logs**: Si algo falla, los logs te dirán exactamente qué pasó
3. **Actualiza fácilmente**: Solo haz `git push` y Render se encarga del resto

---

## 🆘 ¿Problemas?

Si el despliegue falla, revisa:
1. Que `requirements.txt` esté completo
2. Que el comando de inicio sea correcto
3. Los logs de Render para ver el error específico
