;;; hotreload.lsp
;;; SYNCWRAPPER command: Hot Reload for ACP custom scripts
;;;
;;; Change only this line when renaming the script:
(setq *SYNC_SCRIPT_NAME* "hotreload")

(defun c:SYNCWRAPPER ( / ss catalog-pattern )
  ; Step 0: Ensure ACP adapter is loaded
  (arxload "PnP3dACPAdapter.arx")
  (setq catalog-pattern
    (strcat "Plant3DCatalogItem_" *SYNC_SCRIPT_NAME* "*"))
  ; Step 1: Erase existing entities
  (setq ss (ssget "_X" (list '(0 . "INSERT") (cons 2 catalog-pattern))))
  (if ss
    (progn
      (command "ERASE" ss "")
      ; Step 2: Purge block definition cache
      (command "-PURGE" "B" catalog-pattern "N")
    )
  )
  ; Step 3: Regenerate shape with latest impl
  (testacpscript *SYNC_SCRIPT_NAME*)
  (princ)
)

(princ (strcat "\n[SYNCWRAPPER] loaded. Script: " *SYNC_SCRIPT_NAME* "\n"))
(princ)
