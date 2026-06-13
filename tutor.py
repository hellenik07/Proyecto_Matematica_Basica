/* ── BOTÓN DE ABRIR (CON COLOR GRISÁCEO ESTÁTICO) ── */
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

        /* Color de la flecha nativa */
        [data-testid="collapsedControl"] svg {
            fill: #4d4d4d !important;
            color: #4d4d4d !important;
        }
        
        /* Efecto hover */
        [data-testid="collapsedControl"]:hover {
            background-color: #e5e5e5 !important;
            border-color: #9f9f9f !important;
            box-shadow: 0 5px 12px rgba(0,0,0,0.16) !important;
            transform: scale(1.03) !important;
        }