<script setup lang="ts">
const props = defineProps<{
  multiple?: boolean;
  text: string;
}>();

const emit = defineEmits(["fileUpdate"]);

const filesData = ref<
  { name: string; size: number; type: string; lastModified: number }[]
>([]);
function onDrop(files: File[] | null) {
  filesData.value = [];
  if (files) {
    filesData.value = files.map((file) => ({
      file: file,
      name: file.name,
      size: file.size,
      type: file.type,
      lastModified: file.lastModified,
      url: useObjectUrl(file),
    }));
  }
  emit("fileUpdate", filesData.value);
}

const dropZoneRef = ref<HTMLElement>();

const onClick = () => {
  const el = document.createElement("input");
  el.type = "file";
  el.multiple = props.multiple;
  el.onchange = () => {
    if (el.files) {
      onDrop(Array.from(el.files));
    }
  };
  el.click();
};

const { isOverDropZone } = useDropZone(dropZoneRef, onDrop);
</script>

<template>
  <div ref="dropZoneRef" @click="onClick()">
    <div class="dropzone">
      {{ isOverDropZone ? "Drop files here" : props.text }}
    </div>
  </div>
</template>

<style scoped>
.dropzone {
  border: 2px dashed #ccc;
  border-radius: 5px;
  padding: 20px;
  text-align: center;
  color: #ccc;
  transition: all 0.3s ease;
  cursor: pointer;
}

.dropzone.over {
  border-color: #0af;
  color: #0af;
}
</style>
