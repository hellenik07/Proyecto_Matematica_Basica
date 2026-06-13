/* ── BOTÓN DE ABRIR (HAMBURGUESA) ── */
        [data-testid="collapsedControl"] {
            display: flex !important;
            background-color: #f1f1f1 !important;
            border: 2px solid #b8b8b8 !important;
            border-radius: 10px !important;
            margin-top: 15px !important;
            margin-left: 15px !important;
            box-shadow: 0 3px 8px rgba(0,0,0,0.12) !important;
            z-index: 999999 !important;
            width: 48px !important;
            height: 48px !important;
            align-items: center !important;
            justify-content: center !important;
            transition: all 0.2s ease !important;
        }
        
        [data-testid="collapsedControl"]:hover {
            background-color: #e5e5e5 !important;
            border-color: #9f9f9f !important;
            box-shadow: 0 5px 12px rgba(0,0,0,0.16) !important;
            transform: scale(1.03) !important;
        }
        
        [data-testid="collapsedControl"] svg {
            display: none !important; 
        }
        
        [data-testid="collapsedControl"]::after {
            content: "☰" !important;
            color: #5f5f5f !important;
            font-size: 28px !important;
            font-weight: 900 !important;
            font-family: sans-serif !important;
            transition: all 0.2s ease !important;
        }

        /* ── BOTÓN DE CERRAR (X) DENTRO DEL MENÚ LATERAL ── */
        [data-testid="stSidebarCollapseButton"] {
            display: flex !important;
            background-color: #f1f1f1 !important;
            border: 2px solid #b8b8b8 !important;
            border-radius: 10px !important;
            box-shadow: 0 3px 8px rgba(0,0,0,0.12) !important;
            width: 48px !important;
            height: 48px !important;
            align-items: center !important;
            justify-content: center !important;
            transition: all 0.2s ease !important;
            
            /* Asegurar que se posicione bien en la esquina superior derecha del menú */
            position: absolute !important;
            top: 15px !important;
            right: 15px !important;
            z-index: 999999 !important;
        }

        [data-testid="stSidebarCollapseButton"]:hover {
            background-color: #e5e5e5 !important;
            border-color: #9f9f9f !important;
            box-shadow: 0 5px 12px rgba(0,0,0,0.16) !important;
            transform: scale(1.03) !important;
        }

        [data-testid="stSidebarCollapseButton"] svg {
            display: none !important;
        }

        [data-testid="stSidebarCollapseButton"]::after {
            content: "✕" !important;
            font-size: 26px !important;
            color: #4d4d4d !important;
            font-weight: 900 !important;
            font-family: sans-serif !important;
            transition: all 0.2s ease !important;
        }