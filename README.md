# OctoPrint-DetailedProgress

A plugin that sends M117 (and optionally M73) commands to the printer to display the progress of the print job being currently streamed. The message to display can be configured (some placeholders included).
![Example ETA](https://i.imgur.com/ocBp152.jpg)
![Example ETL](https://i.imgur.com/oJiMm2p.jpg)
![Example Percent](https://i.imgur.com/McaCNsx.jpg)
![Example M73 Prusa](https://i.imgur.com/C1zeANH.jpg)

## Setup

Install via the bundled [Plugin Manager](https://github.com/foosel/OctoPrint/wiki/Plugin:-Plugin-Manager)
or manually using this URL:

    https://github.com/dattas/OctoPrint-DetailedProgress/archive/master.zip

## Configuration

``` yaml
plugins:
  detailedprogress:
    # Number of seconds (minimum) to rotate the messages
    time_to_change: 10
    eta_strftime: "%H:%M:%S Day %d"
    etl_format: "{hours:02d}:{minutes:02d}:{seconds:02d}"
    # Send M73 progress commands 
    use_M73: true
    # M73 commands syntax specific for Prusa Firmware (>=3.3.0)
    M73_PrusaStyle: true
    # Messages to display. Placeholders:
    # - completion : The % completed
    # - printTimeLeft : A string in the format "HH:MM:SS" with how long the print still has left
    # - ETA : The date and time formatted in "%H:%M:%S Day %d" that the print is estimated to be completed
    # - filepos: The current position in the file currently being printed
    messages:
      - "{completion:.2f}% complete"
      - "ETL: {printTimeLeft}"
      - "ETA: {ETA}"
```
