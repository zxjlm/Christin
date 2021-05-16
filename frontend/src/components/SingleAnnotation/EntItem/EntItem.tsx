import './index.css';
import { CloseOutlined } from '@ant-design/icons';
import type { labelType } from '../index';
import { Dropdown, Menu } from 'antd';
import { useState } from 'react';
import { useModel } from '@@/plugin-model/useModel';

interface EntItemProps {
  content: string;
  label: string | null;
  color: string;
  labels: labelType[];
  // updateEntity: (labelId: number, annotationId: number) => void;
  item_id: number | undefined;
  list_id: number;
  readOnly: boolean;
}

export default ({ content, label, color, labels, item_id, list_id, readOnly }: EntItemProps) => {
  const [showMenu, setShowMenu] = useState(false);
  // @ts-ignore
  const { updateEntity } = useModel('nerDocs', (model) => ({ updateEntity: model.updateEntity }));

  const idealColor = function (hexString: string) {
    const r = parseInt(hexString.substr(1, 2), 16);
    const g = parseInt(hexString.substr(3, 2), 16);
    const b = parseInt(hexString.substr(5, 2), 16);
    return (r * 299 + g * 587 + b * 114) / 1000 < 128 ? '#ffffff' : '#000000';
  };

  const onClick = () => {
    // if (item_id) deleteAnnotation(item_id)
  };

  if (readOnly) {
    return (
      <span className="highlight bottom" style={{ borderColor: color }}>
        <span className="highlight__content">{content}</span>
        <span
          data-label={label}
          className="highlight__label"
          style={{ backgroundColor: color, color: idealColor(color) }}
          onClick={() => setShowMenu(!showMenu)}
        />
      </span>
    );
  }

  return (
    <span className="highlight bottom" style={{ borderColor: color }}>
      <span className="highlight__content">
        {content}
        <button type="button" className={'delete'} onClick={onClick} name={`close${item_id}`}>
          <CloseOutlined />
        </button>
      </span>
      <Dropdown
        overlay={
          <Menu>
            {labels.map((item) => (
              <Menu.Item
                key={item.id}
                onClick={() => {
                  if (typeof item_id !== undefined && item_id !== undefined) {
                    updateEntity(item.id, item_id, list_id);
                  }
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
        <span
          data-label={label}
          className="highlight__label"
          style={{ backgroundColor: color, color: idealColor(color) }}
          onClick={() => setShowMenu(!showMenu)}
        />
      </Dropdown>
    </span>
  );
};
