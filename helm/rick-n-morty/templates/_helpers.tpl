{{- define "rick-n-morty.name" -}}
{{ .Chart.Name }}
{{- end -}}

{{- define "rick-n-morty.fullname" -}}
{{ include "rick-n-morty.name" . }}-{{ .Release.Name }}
{{- end -}}