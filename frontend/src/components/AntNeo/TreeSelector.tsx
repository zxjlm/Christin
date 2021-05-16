import { TreeSelect } from 'antd';
import { DataNode } from 'rc-tree-select/lib/interface';

const { SHOW_PARENT } = TreeSelect;

export const TreeSelector = ({ options }: { options: DataNode[] }) => {
  const onChange = () => {};

  return (
    <TreeSelect
      treeData={options}
      onChange={onChange}
      treeCheckable={true}
      showCheckedStrategy={SHOW_PARENT}
      placeholder={'Please select'}
      allowClear={true}
      style={{
        width: '100%',
      }}
    />
  );
};
