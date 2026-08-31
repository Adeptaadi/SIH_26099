import { useState } from 'react';

export default function useMatches() {
  const [matches] = useState([]);
  return { matches };
}
