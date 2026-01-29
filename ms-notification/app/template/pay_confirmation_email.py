def html_pay_confirmation(game_name, folio):
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Confirmación de Compra</title>
    </head>
    <body style="margin: 0; padding: 0; background-color: #f4f4f5; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;">
        
        <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" style="background-color: #f4f4f5; padding: 40px 0;">
            <tr>
                <td align="center">
                    
                    <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" style="max-width: 600px; background-color: #ffffff; border-radius: 12px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); overflow: hidden;">
                        
                        <tr>
                            <td style="background-color: #2563eb; padding: 30px; text-align: center;">
                                <h1 style="margin: 0; color: #ffffff; font-size: 28px; font-weight: 800; letter-spacing: 2px; text-transform: uppercase;">
                                    GAME<span style="color: #93c5fd;">STORE</span> 🎮
                                </h1>
                            </td>
                        </tr>

                        <tr>
                            <td style="padding: 40px 30px; text-align: center;">
                                <h2 style="margin: 0 0 20px 0; color: #1f2937; font-size: 24px;">¡Excelente elección!</h2>
                                <p style="margin: 0 0 30px 0; color: #4b5563; font-size: 16px; line-height: 1.5;">
                                    Tu compra ha sido confirmada exitosamente. Ya estamos preparando tu clave de activación.
                                </p>

                                <div style="background-color: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 20px; text-align: left; display: inline-block; width: 100%; box-sizing: border-box;">
                                    <table width="100%" border="0">
                                        <tr>
                                            <td style="color: #64748b; font-size: 12px; text-transform: uppercase; font-weight: bold; padding-bottom: 5px;">Juego Adquirido</td>
                                        </tr>
                                        <tr>
                                            <td style="color: #111827; font-size: 18px; font-weight: 600; padding-bottom: 15px;">{game_name}</td>
                                        </tr>
                                        <tr>
                                            <td style="border-top: 1px dashed #cbd5e1; padding-top: 15px; color: #64748b; font-size: 12px; text-transform: uppercase; font-weight: bold; padding-bottom: 5px;">Folio de Transacción</td>
                                        </tr>
                                        <tr>
                                            <td style="color: #2563eb; font-family: 'Courier New', monospace; font-size: 16px; letter-spacing: 1px;">{folio}</td>
                                        </tr>
                                    </table>
                                </div>

                                <p style="margin-top: 30px; color: #9ca3af; font-size: 14px;">
                                    Si tienes alguna duda, responde a este correo con tu folio.
                                </p>
                            </td>
                        </tr>

                        <tr>
                            <td style="background-color: #1f2937; padding: 20px; text-align: center;">
                                <p style="margin: 0; color: #9ca3af; font-size: 12px;">
                                    &copy; 2026 Game Store Inc. Todos los derechos reservados.
                                </p>
                            </td>
                        </tr>

                    </table>
                </td>
            </tr>
        </table>

    </body>
    </html>
    """