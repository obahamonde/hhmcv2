  
<script setup lang="ts">
import { usePianoStore, useSequencerStore } from '~/composables';
import { midiNoteToString } from '~/composables/midinote';
const store = usePianoStore()
const sequencerStore = useSequencerStore()

const props = defineProps({
  positionInMelody: Number,
  synth: null
})

const determineColor = (note: number) => {
  if (note === sequencerStore.getNoteAtPosition(props.positionInMelody)) {
    if (store.playPosition === props.positionInMelody && store.sequencerPlaying)
      return 'noteBoxSelectedPlaying playing'
    return 'noteBoxSelected'
  }
  if (note % 2 === 0) {
    if (store.playPosition === props.positionInMelody && store.sequencerPlaying)
      return 'noteBoxLightPlaying playing'
    return 'noteBoxLight'
  }
  if (store.playPosition === props.positionInMelody && store.sequencerPlaying)
    return 'noteBoxDarkPlaying playing'
  return 'noteBoxDark'
}

const selectNote = (note: number) => {
  // If clicking the same note, deselect it instead
  if (note === sequencerStore.getNoteAtPosition(props.positionInMelody)) {
    sequencerStore.changeNoteAtPosition(props.positionInMelody, 0)
  } else {
    // play note
    props.synth.triggerAttackRelease(midiNoteToString(note), "8n");
    sequencerStore.changeNoteAtPosition(props.positionInMelody, note)
  }
}

</script>

<template>
  <div>
    <div v-for="note in sequencerStore.notes" class="noteBox" :class="determineColor(note)" @click="selectNote(note)" />
  </div>
</template>

<style scoped lang="sass">
  .noteBox
    height: 22px
    width: 40px
    border-left: 1px solid #24343e
    border-top: 1px solid #24343e
    //transition: background-color 0.2s
  
  .noteBox:hover
    background-color: #3e6364
  
  .noteBoxLight
    background-color: #34444e
  
  .noteBoxDark
    background-color: #2e3e48
  
  .noteBoxLightPlaying
    background-color: #3a656e
  
  .noteBoxDarkPlaying
    background-color: #3a656e
  
  .noteBoxSelected
    background-color: #59c277
  
  .noteBoxSelectedPlaying
    background-color: #dcea18
  
  .noteBoxSelected:hover
    background-color: #59c277
  
  .playing
    border-left: none
    border-top: none
  </style>
  