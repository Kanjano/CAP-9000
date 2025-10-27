; CAP 9000 Custom NSIS Installer Script
; Gestisce download Ollama e documentazioni

!include "MUI2.nsh"
!include "FileFunc.nsh"

; Variabili globali
Var OllamaInstalled
Var DownloadDocs
Var RequiredSpace
Var AvailableSpace

; Pagina personalizzata per opzioni
Page custom CustomOptionsPage CustomOptionsPageLeave

; Funzione per calcolare spazio richiesto
Function CalculateRequiredSpace
    ; CAP 9000 app: ~200 MB
    ; Ollama: ~450 MB
    ; CodeLlama model: ~3800 MB
    ; Documentazioni: ~50 MB
    ; TOTALE: ~4500 MB = 4.5 GB
    
    StrCpy $RequiredSpace "4500" ; MB
    
    ; Verifica spazio disponibile
    ${GetRoot} "$INSTDIR" $0
    ${DriveSpace} "$0" "/D=F /S=M" $AvailableSpace
    
    ; Converti in MB per confronto
    IntOp $AvailableSpace $AvailableSpace * 1
    
    ; Verifica se c'è abbastanza spazio
    IntCmp $AvailableSpace $RequiredSpace SpaceOK SpaceOK SpaceError
    
    SpaceOK:
        Return
    
    SpaceError:
        MessageBox MB_OK|MB_ICONEXCLAMATION "Spazio insufficiente sul disco.$\n$\nRichiesto: $RequiredSpace MB (~4.5 GB)$\nDisponibile: $AvailableSpace MB$\n$\nLibera spazio e riprova."
        Abort
FunctionEnd

; Pagina opzioni personalizzata
Function CustomOptionsPage
    !insertmacro MUI_HEADER_TEXT "Opzioni di Installazione" "Configura i componenti da installare"
    
    nsDialogs::Create 1018
    Pop $0
    
    ${If} $0 == error
        Abort
    ${EndIf}
    
    ; Titolo
    ${NSD_CreateLabel} 0 0 100% 20u "CAP 9000 richiede i seguenti componenti:"
    Pop $0
    
    ; Info spazio
    ${NSD_CreateGroupBox} 0 30u 100% 80u "Spazio su Disco Richiesto"
    Pop $0
    
    ${NSD_CreateLabel} 10u 45u 90% 12u "• CAP 9000 Application: ~200 MB"
    Pop $0
    
    ${NSD_CreateLabel} 10u 60u 90% 12u "• Ollama LLM Engine: ~450 MB"
    Pop $0
    
    ${NSD_CreateLabel} 10u 75u 90% 12u "• CodeLlama AI Model: ~3.8 GB"
    Pop $0
    
    ${NSD_CreateLabel} 10u 90u 90% 12u "• Official Documentation: ~50 MB"
    Pop $0
    
    ${NSD_CreateLabel} 10u 105u 90% 15u "TOTALE: ~4.5 GB" 
    Pop $0
    SetCtlColors $0 FF0000 transparent
    
    ; Checkbox Ollama
    ${NSD_CreateCheckbox} 0 120u 100% 12u "Installa Ollama e CodeLlama (Raccomandato)"
    Pop $OllamaInstalled
    ${NSD_Check} $OllamaInstalled
    
    ; Checkbox Docs
    ${NSD_CreateCheckbox} 0 135u 100% 12u "Scarica documentazioni ufficiali (Raccomandato)"
    Pop $DownloadDocs
    ${NSD_Check} $DownloadDocs
    
    ; Note
    ${NSD_CreateLabel} 0 155u 100% 30u "Nota: Senza Ollama, CAP 9000 funzionerà in modalità limitata.$\nSenza documentazioni, userà le best practices integrate."
    Pop $0
    SetCtlColors $0 808080 transparent
    
    nsDialogs::Show
FunctionEnd

Function CustomOptionsPageLeave
    ; Salva le scelte
    ${NSD_GetState} $OllamaInstalled $OllamaInstalled
    ${NSD_GetState} $DownloadDocs $DownloadDocs
    
    ; Ricalcola spazio in base alle scelte
    StrCpy $RequiredSpace "200" ; Base app
    
    ${If} $OllamaInstalled == ${BST_CHECKED}
        IntOp $RequiredSpace $RequiredSpace + 4250 ; Ollama + Model
    ${EndIf}
    
    ${If} $DownloadDocs == ${BST_CHECKED}
        IntOp $RequiredSpace $RequiredSpace + 50 ; Docs
    ${EndIf}
    
    ; Verifica spazio
    Call CalculateRequiredSpace
FunctionEnd

; Macro per download Ollama
!macro DownloadOllama
    ${If} $OllamaInstalled == ${BST_CHECKED}
        DetailPrint "Downloading Ollama..."
        
        ; Crea directory temporanea
        CreateDirectory "$TEMP\cap9000-setup"
        
        ; Download Ollama
        NSISdl::download "https://ollama.ai/download/OllamaSetup.exe" "$TEMP\cap9000-setup\OllamaSetup.exe"
        Pop $0
        
        ${If} $0 == "success"
            DetailPrint "Installing Ollama..."
            ExecWait '"$TEMP\cap9000-setup\OllamaSetup.exe" /S'
            
            ; Attendi che Ollama sia installato
            Sleep 3000
            
            DetailPrint "Starting Ollama service..."
            Exec '"$PROGRAMFILES\Ollama\ollama.exe" serve'
            
            Sleep 5000
            
            DetailPrint "Downloading CodeLlama model (this may take several minutes)..."
            ExecWait '"$PROGRAMFILES\Ollama\ollama.exe" pull codellama'
            
            DetailPrint "Ollama setup completed!"
        ${Else}
            DetailPrint "Warning: Ollama download failed. You can install it manually from https://ollama.ai"
        ${EndIf}
        
        ; Cleanup
        Delete "$TEMP\cap9000-setup\OllamaSetup.exe"
        RMDir "$TEMP\cap9000-setup"
    ${EndIf}
!macroend

; Macro per download documentazioni
!macro DownloadDocumentation
    ${If} $DownloadDocs == ${BST_CHECKED}
        DetailPrint "Downloading official documentation..."
        
        ; Verifica Python
        nsExec::ExecToStack 'python --version'
        Pop $0
        Pop $1
        
        ${If} $0 == 0
            ; Python trovato, scarica docs
            DetailPrint "Python found, downloading documentation..."
            nsExec::ExecToLog 'python "$INSTDIR\download_docs.py"'
            DetailPrint "Documentation download completed!"
        ${Else}
            DetailPrint "Warning: Python not found. Documentation will not be downloaded."
            DetailPrint "You can download it later by running: python download_docs.py"
        ${EndIf}
    ${EndIf}
!macroend

; Sezione principale installazione
Section "Install"
    SetOutPath "$INSTDIR"
    
    ; Copia file applicazione
    File /r "${BUILD_RESOURCES_DIR}\*.*"
    
    ; Crea shortcuts
    CreateDirectory "$SMPROGRAMS\CAP 9000"
    CreateShortCut "$SMPROGRAMS\CAP 9000\CAP 9000.lnk" "$INSTDIR\CAP 9000.exe"
    CreateShortCut "$DESKTOP\CAP 9000.lnk" "$INSTDIR\CAP 9000.exe"
    
    ; Scrivi uninstaller
    WriteUninstaller "$INSTDIR\Uninstall.exe"
    
    ; Aggiungi a Add/Remove Programs
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\CAP9000" "DisplayName" "CAP 9000"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\CAP9000" "UninstallString" "$INSTDIR\Uninstall.exe"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\CAP9000" "DisplayIcon" "$INSTDIR\CAP 9000.exe"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\CAP9000" "Publisher" "Antonio Cangiano"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\CAP9000" "DisplayVersion" "1.0.0"
    WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\CAP9000" "EstimatedSize" $RequiredSpace
    
    ; Download e installa componenti
    !insertmacro DownloadOllama
    !insertmacro DownloadDocumentation
    
SectionEnd

; Sezione uninstall
Section "Uninstall"
    ; Rimuovi file
    RMDir /r "$INSTDIR"
    
    ; Rimuovi shortcuts
    Delete "$DESKTOP\CAP 9000.lnk"
    RMDir /r "$SMPROGRAMS\CAP 9000"
    
    ; Rimuovi da registry
    DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\CAP9000"
    
    MessageBox MB_YESNO "Vuoi rimuovere anche Ollama?" IDYES RemoveOllama IDNO SkipOllama
    
    RemoveOllama:
        ExecWait '"$PROGRAMFILES\Ollama\Uninstall.exe" /S'
    
    SkipOllama:
    
SectionEnd

; Funzione di inizializzazione
Function .onInit
    ; Verifica se già installato
    ReadRegStr $0 HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\CAP9000" "UninstallString"
    ${If} $0 != ""
        MessageBox MB_YESNO "CAP 9000 è già installato. Vuoi disinstallarlo prima?" IDYES Uninstall IDNO Continue
        
        Uninstall:
            ExecWait '$0 _?=$INSTDIR'
            Goto Continue
        
        Continue:
    ${EndIf}
    
    ; Calcola spazio iniziale
    Call CalculateRequiredSpace
FunctionEnd
