export const counterReducer = (state = 0, action: { type: string }) => {
  switch (action.type) {
    case 'INIT':
      return state + 1;
    case 'ADD':
      return state - 1;
    case 'UPDATE':
      return 0;
    case 'DELETE':
      return 0;
    default:
      // if none of the above matches, code comes here
      return state;
  }
};
