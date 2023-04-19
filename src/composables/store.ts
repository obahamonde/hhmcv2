import { defineStore, acceptHMRUpdate } from "pinia";

type NotifyProps = {
  message: string;
  status: "success" | "error" | "info";
};

export const useStore = defineStore("state", () => {
  const state = reactive({
    notifications: [] as NotifyProps[],
    user: {} as any,
  });
  const setState = (newState: any) => {
    Object.assign(state, newState);
  };

  const notify = (message: string, status: "success" | "error" | "info") => {
    state.notifications.push({ message, status });
  };

  return {
    state,
    setState,
    notify
  };
});

if (import.meta.hot) {
  import.meta.hot.accept(acceptHMRUpdate(useStore, import.meta.hot));
}
