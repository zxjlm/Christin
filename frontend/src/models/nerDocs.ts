import { useCallback, useState } from 'react';
import type { annotationType } from '@/components/SingleAnnotation';
import type { BasicAPI } from '@/services/site-data/typings';

export default () => {
  const [nerDocs, setNerDocs] = useState<BasicAPI.nerDoc[]>([]);
  const removeEntityHandler = (annotationId: number, list_id: number) => {
    const tmpDocs = [...nerDocs];
    nerDocs[list_id].annotations = nerDocs[list_id].annotations.filter(
      (item) => item.id !== annotationId,
    );
    setNerDocs(tmpDocs);
  };
  const updateEntityHandler = (labelId: number, annotationId: number, list_id: number) => {
    const tmp = [...nerDocs];
    const index = nerDocs[list_id].annotations.findIndex((item) => item.id === annotationId);
    tmp[list_id].annotations[index].label = labelId;
    setNerDocs(tmp);
  };
  const addEntityHandler = (startOffset: any, endOffset: any, labelId: any, list_id: number) => {
    const payload: annotationType = {
      id: Math.floor(Math.random() * Math.floor(Number.MAX_SAFE_INTEGER)),
      startOffset,
      endOffset,
      label: labelId,
    };
    const tmpDocs = [...nerDocs];
    nerDocs[list_id].annotations.push(payload);
    setNerDocs(tmpDocs);
  };

  const addEntity = useCallback(addEntityHandler, [nerDocs]);
  const deleteEntity = useCallback(removeEntityHandler, [nerDocs]);
  const updateEntity = useCallback(updateEntityHandler, [nerDocs]);

  return { nerDocs, setNerDocs, addEntity, deleteEntity, updateEntity };
};
