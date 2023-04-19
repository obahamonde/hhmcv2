const notes = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

export const midiNoteToString = (note:number) => {
    let octave = Math.floor(note / 12) - 1;
    let noteName = notes[note % 12]

    return noteName + octave.toString()
}
