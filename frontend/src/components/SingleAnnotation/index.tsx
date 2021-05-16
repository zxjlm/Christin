import { useEffect, useState } from 'react';
import EntItem from './EntItem/EntItem';
import 'antd/dist/antd.css';
import './index.css';
import { Dropdown, Menu } from 'antd';
import { useModel } from '@@/plugin-model/useModel';

export interface labelType {
  id: number;
  text: string;
  prefixKey: null;
  suffixKey: string;
  backgroundColor: string;
  textColor: string;
}

export interface annotationType {
  id: number;
  label: number;
  startOffset: number;
  endOffset: number;
}

interface EntItemBoxProps {
  labels: labelType[];
  text: string;
  list_id: number;
  readOnly?: boolean;
}

interface chunkState {
  id?: number;
  label: string | null;
  color: string;
  text: string;
  newline?: boolean;
}

export default ({ labels, text, list_id, readOnly = false }: EntItemBoxProps) => {
  const [renderChunks, setRenderChunks] = useState<chunkState[]>([]);
  const [position, setPosition] = useState({ start: 0, end: 0, x: 0, y: 0 });
  const [showMenu, setShowMenu] = useState(false);

  const { nerDocs, addEntity, deleteAnnotation } = useModel('nerDocs', (model) => ({
    nerDocs: model.nerDocs,
    addEntity: model.addEntity,
    deleteAnnotation: model.deleteEntity,
  }));

  const sortedEntities: () => annotationType[] = () => {
    return nerDocs[list_id].annotations
      .slice()
      .sort(
        (a: { startOffset: number }, b: { startOffset: number }) => a.startOffset - b.startOffset,
      );
  };
  const labelObject: () => Record<string, { text: string; backgroundColor: string }> = () => {
    const obj: any = {};
    // eslint-disable-next-line no-restricted-syntax
    for (const label of labels) {
      obj[label.id] = label;
    }
    return obj;
  };
  const makeChunks = (rawText: string) => {
    const chunks = [];
    const snippets = rawText.split('\n');
    // eslint-disable-next-line no-restricted-syntax
    for (const snippet of snippets.slice(0, -1)) {
      chunks.push({
        label: null,
        color: null,
        text: `${snippet}\n`,
        newline: false,
      });
      chunks.push({
        label: null,
        color: null,
        text: '',
        newline: true,
      });
    }
    chunks.push({
      label: null,
      color: null,
      text: snippets.slice(-1)[0],
      newline: false,
    });
    return chunks;
  };
  const chunks: () => chunkState[] = () => {
    let inner_chunks: any[] = [];
    let startOffset = 0;
    // to count the number of characters correctly.
    const characters = [...text];
    // eslint-disable-next-line no-restricted-syntax
    for (const entity of sortedEntities()) {
      // add non-entities to chunks.
      let piece = characters.slice(startOffset, entity.startOffset).join('');
      inner_chunks = inner_chunks.concat(makeChunks(piece));
      startOffset = entity.endOffset;
      // add entities to chunks.
      const label = labelObject()[entity.label];
      piece = characters.slice(entity.startOffset, entity.endOffset).join('');
      inner_chunks.push({
        id: entity.id,
        label: label.text,
        color: label.backgroundColor,
        text: piece,
      });
    }
    // add the rest of text.
    inner_chunks = inner_chunks.concat(
      makeChunks(characters.slice(startOffset, characters.length).join('')),
    );
    return inner_chunks;
  };

  const setSpanInfo = (e: any) => {
    let selection;
    // Modern browsers.
    if (window.getSelection) {
      selection = window.getSelection();
    } else if (document.getSelection()) {
      selection = document.getSelection();
    }
    if (
      !selection ||
      e.target.className !== 'highlight-container highlight-container--bottom-labels'
    ) {
      return { start_: 0, end_: 0 };
    }

    const range = selection.getRangeAt(0);
    const preSelectionRange = range.cloneRange();
    preSelectionRange.selectNodeContents(e.target);
    preSelectionRange.setEnd(range.startContainer, range.startOffset);
    const start_tmp = [...preSelectionRange.toString()].length;
    const end_tmp = start_tmp + [...range.toString()].length;

    return { start_tmp, end_tmp };
  };
  const validateSpan = (
    start_: number | undefined = position.start,
    end_: number | undefined = position.end,
  ) => {
    if (typeof start_ === 'undefined' || typeof end_ === 'undefined' || end_ === 0) {
      setPosition({ ...position });
      setShowMenu(false);
      return false;
    }
    if (start_ === end_) {
      setPosition({ ...position });
      setShowMenu(false);
      return false;
    }
    // eslint-disable-next-line no-restricted-syntax
    for (const entity of nerDocs[list_id].annotations) {
      if (entity.startOffset <= start_ && start_ < entity.endOffset) {
        return false;
      }
      if (entity.startOffset < end_ && end_ <= entity.endOffset) {
        return false;
      }
      if (start_ < entity.startOffset && entity.endOffset < end_) {
        return false;
      }
    }
    return true;
  };
  const show = (e: any, start_: number, end_: number) => {
    e.preventDefault();
    const tmp = {
      start: start_,
      end: end_,
      x: e.clientX || e.changedTouches[0].clientX,
      y: e.clientY || e.changedTouches[0].clientY,
      // showMenu: true,
    };
    setPosition(tmp);
    setShowMenu(true);
  };
  const handleOpen = (e: any) => {
    e.preventDefault();
    const deleteElem = e.path.filter((elem: any) => elem.className === 'delete');
    if (deleteElem.length !== 0) {
      const inner_id = Number(deleteElem[0].name.replace('close', ''));
      deleteAnnotation(inner_id, list_id);
    } else if (e.target.className === 'highlight__label') {
      // eslint-disable-next-line no-console
      console.log('open trigger', e);
    } else {
      const { start_tmp, end_tmp } = setSpanInfo(e);
      if (validateSpan(start_tmp, end_tmp) && start_tmp && end_tmp) {
        show(e, start_tmp, end_tmp);
      }
    }
  };

  useEffect(() => {
    const cls = document.getElementsByClassName(
      'highlight-container highlight-container--bottom-labels',
    );
    if (typeof nerDocs[list_id] !== 'undefined') {
      setRenderChunks(chunks());
      if (!readOnly) {
        cls[list_id].addEventListener('mouseup', handleOpen);
      }
    }
    return () => {
      if (cls[list_id]) cls[list_id].removeEventListener('mouseup', handleOpen);
    };
  }, [nerDocs]);

  if (readOnly) {
    return (
      <div className={'highlight-container highlight-container--bottom-labels'}>
        {renderChunks.map((chunk) => {
          if (chunk.color)
            return (
              <EntItem
                key={chunk.id}
                labels={labels}
                label={chunk.label}
                color={chunk.color}
                content={chunk.text}
                item_id={chunk.id}
                list_id={list_id}
                readOnly={readOnly}
              />
            );
          return chunk.text;
        })}
      </div>
    );
  }

  return (
    <div className={'highlight-container highlight-container--bottom-labels'}>
      {renderChunks.map((chunk) => {
        if (chunk.color)
          return (
            <EntItem
              key={chunk.id}
              labels={labels}
              label={chunk.label}
              color={chunk.color}
              content={chunk.text}
              item_id={chunk.id}
              list_id={list_id}
              readOnly={readOnly}
            />
          );
        return chunk.text;
      })}
      <Dropdown
        overlay={
          <Menu style={{ position: 'fixed', top: `${position.y}px`, left: `${position.x}px` }}>
            {labels.map((item) => (
              <Menu.Item
                key={item.id}
                onClick={() => {
                  addEntity(position.start, position.end, item.id, list_id);
                  setShowMenu(false);
                }}
              >
                {item.text}
              </Menu.Item>
            ))}
          </Menu>
        }
        placement="bottomLeft"
        visible={showMenu}
      >
        <div />
      </Dropdown>
    </div>
  );
};
