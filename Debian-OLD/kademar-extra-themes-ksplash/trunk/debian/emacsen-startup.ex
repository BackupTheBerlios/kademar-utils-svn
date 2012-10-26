;; -*-emacs-lisp-*-
;;
;; Emacs startup file, e.g.  /etc/emacs/site-start.d/50kademar-extra-themes-ksplash.el
;; for the Debian kademar-extra-themes-ksplash package
;;
;; Originally contributed by Nils Naumann <naumann@unileoben.ac.at>
;; Modified by Dirk Eddelbuettel <edd@debian.org>
;; Adapted for dh-make by Jim Van Zandt <jrv@debian.org>

;; The kademar-extra-themes-ksplash package follows the Debian/GNU Linux 'emacsen' policy and
;; byte-compiles its elisp files for each 'emacs flavor' (emacs19,
;; xemacs19, emacs20, xemacs20...).  The compiled code is then
;; installed in a subdirectory of the respective site-lisp directory.
;; We have to add this to the load-path:
(let ((package-dir (concat "/usr/share/"
                           (symbol-name flavor)
                           "/site-lisp/kademar-extra-themes-ksplash")))
;; If package-dir does not exist, the kademar-extra-themes-ksplash package must have
;; removed but not purged, and we should skip the setup.
  (when (file-directory-p package-dir)
        (setq load-path (cons package-dir load-path))
       (autoload 'kademar-extra-themes-ksplash-mode "kademar-extra-themes-ksplash-mode"
         "Major mode for editing kademar-extra-themes-ksplash files." t)
       (add-to-list 'auto-mode-alist '("\\.kademar-extra-themes-ksplash$" . kademar-extra-themes-ksplash-mode))))

