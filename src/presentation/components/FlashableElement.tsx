import clsx from "clsx";
import type {
  ComponentPropsWithoutRef,
  ElementType,
  PropsWithChildren,
} from "react";
import { useEffect, useState } from "react";

type PolymorphicAsProp<E extends ElementType> = {
  as?: E;
};

type PolymorphicProps<E extends ElementType> = PropsWithChildren<
  ComponentPropsWithoutRef<E> & PolymorphicAsProp<E>
>;

const defaultElement = "div";

type FlashableElementProps<E extends ElementType = typeof defaultElement> =
  PolymorphicProps<E> & {
    dependentVar?: unknown;
  };

/**
 *
 * @param children
 * @param dependentVar this variable is used to trigger yellow flash animation (re-render)
 * @returns a span element with yellow flash animation
 */
function FlashableElement<E extends ElementType = typeof defaultElement>({
  as,
  children,
  className,
  dependentVar,
  ...restProps
}: FlashableElementProps<E>) {
  const Component = as ?? defaultElement;

  const [key, setKey] = useState<string>();

  useEffect(() => {
    setKey(crypto.randomUUID());
  }, [dependentVar ?? children]);

  return (
    <Component
      key={key}
      {...restProps}
      className={clsx("animate-fade-yellow rounded", className)}
    >
      {children}
    </Component>
  );
}

export default FlashableElement;
