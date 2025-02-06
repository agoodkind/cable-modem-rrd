import js from "@eslint/js";
import prettier from "eslint-plugin-prettier";
import reactHooks from "eslint-plugin-react-hooks";
import reactRefresh from "eslint-plugin-react-refresh";
import globals from "globals";
import tseslint from "typescript-eslint";

export default tseslint.config(
	{ ignores: ["dist"] },
	{
		extends: [
			js.configs.recommended,
			...tseslint.configs.recommended,
			"prettier", // disable ESLint rules that conflict with Prettier
		],
		files: ["**/*.{ts,tsx}"],
		languageOptions: {
			ecmaVersion: 2020,
			globals: globals.browser,
		},
		plugins: {
			"react-hooks": reactHooks,
			"react-refresh": reactRefresh,
			prettier: prettier,
		},
		rules: {
			...reactHooks.configs.recommended.rules,
			"react-refresh/only-export-components": [
				"warn",
				{ allowConstantExport: true },
			],
			"no-unused-vars": "warn",
			"no-console": "warn",
			"react-hooks/exhaustive-deps": "off",
			"prettier/prettier": "warn", // reports Prettier formatting issues as warnings
		},
	}
);
