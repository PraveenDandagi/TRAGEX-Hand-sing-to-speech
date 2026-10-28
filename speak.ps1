param(
    [Parameter(Mandatory = $true, Position = 0)]
    [string]$Text
)

Add-Type -AssemblyName System.Speech

$speech = New-Object System.Speech.Synthesis.SpeechSynthesizer
$speech.Volume = 100
$speech.Rate = 0
$speech.Speak($Text)
